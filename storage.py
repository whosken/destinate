import logging, unittest
import os
import json
import requests
from collections import namedtuple
from util import load_config

Place = namedtuple('Place', 'name, intro, body, profile')
Topic = namedtuple('Topic', 'profile, members')

class BaseStorage(object):
    """
    An abstract class for CouchDb-based database access
    """

    def __init__(self):
        try:
            config = load_config()[self.db_name]
            self.server = config['server']
            self.key = (config['username'], config['password'])
            logging.info('Database <{0}> connection opened'.format(self.db_name))
        except AttributeError, e:
            if self.__class__ is BaseStorage:
                logging.error('BaseStorage is meant to be abstract')
            raise
        except KeyError, e:
            logging.error('Missing database setting in config')
            raise
            
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        pass
            
    def  _get_object_url(self, object_id):
        return '/'.join((self.server, self.db_name, object_id))
        
    def _handle_bad_request(self, object_id, data):
        logging.error('Unable to store object <{0}> with data <{1}>'.format(object_id, repr(data)))
    
    def _handle_not_found(self, object_id, data):
        logging.error('Unable to get object <{0}>'.format(object_id))
        
    def _handle_conflict(self, object_id, data):
        revision = self.head_object_revision(object_id)
        return self.put_object(object_id, data, revision = revision)
    
    handle_response = {
            '400': _handle_bad_request,
            '404': _handle_not_found,
            '409': _handle_conflict,
        }
    
    def _handle_response(self, response, object_id, data=None):
        if str(response.status_code) in self.handle_response:
            return self.handle_response[str(response.status_code)](self, object_id, data)
        return response.content
    
    def put_object(self, object_id, data, revision = None):
        url = self._get_object_url(object_id)
        if revision: data['_rev'] = revision
        response = requests.put(url, auth=self.key, data=json.dumps(data))
        return self._handle_response(response, object_id, data)
        
    def get_object(self, object_id):
        url = self._get_object_url(object_id)
        response = requests.get(url, auth=self.key)
        return self._handle_response(response, object_id)
        
    def head_object_revision(self, object_id):
        url = self._get_object_url(object_id)
        response = requests.head(url, auth=self.key)
        if 'Etag' in response.headers:
            return response.headers['Etag'].replace('"','')
    
    def _get_view(self, design_name, view_name, view_params):
        view_id = '/'.join(('_design', design_name, '_view', view_name))
        url = '/'.join((self.server, self.db_name, view_id))
        if view_params:
            url += '?' + '&'.join('{0}={1}'.format(key,value) for key,value in view_params.items())
        response = requests.get(url, auth=self.key)
        return response.content
        
    def _yield_view_response(self, content):
        for row in json.loads(content).get('rows',[]):
            if 'value' in row:
                yield row['value']
        
    def get_all_ids(self):
        result = self.get_object('_all_docs')
        for row in json.loads(result).get('rows',[]):
            if row['id'][0] == '_': continue
            yield row['id']
        
    def get_all_objects(self):
        for doc_id in self.get_all_ids():
            yield self.get_object(doc_id)
            
    def compact(self):
        object_id = '_compact'
        url = self._get_object_url(object_id)
        response = requests.post(url, auth=self.key, headers={'Content-Type': 'application/json'})
        return self._handle_response(response, object_id)


class PlaceStorage(BaseStorage):
    db_name = 'place_store'
    
    def put_place(self, place):
        if not isinstance(place,Place):
            place = Place(*place)
        return self.put_object(place[0], place._asdict())
    
    def put_places(self, places):
        for place in places:
            yield self.put_place(place)
            
    def get_place(self, place_id):
        object = self.get_object(place_id)
        if object:
            return self.json_to_place(object)
    
    def get_all_places(self):
        for object in self.get_all_objects():
            yield self.json_to_place(object)
    
    def get_places(self, place_ids):
        for place_id in place_ids:
            yield self.get_place(place_id)
    
    def get_places_by_word(self, word):
        response = self._get_view('find_docs', 'by_keyword', {'key':json.dumps(word)})
        def get_place_ids():
            for place_ids in self._yield_view_response(response):
                for place_id in place_ids:
                    yield place_id
                    
        return self.get_places(get_place_ids())
    
    def get_places_by_words(self, words):
        places = {}
        for word in words:
            for place in self.get_places_by_word(word):
                if place.name not in places:
                    places[place.name] = place
        return places.itervalues()
    
    def json_to_place(self, place_json):
        place_dict = json.loads(place_json)
        return Place(
            name=place_dict['name'],
            intro=place_dict['intro'],
            body=place_dict['body'],
            profile=place_dict['profile'])

class TopicStorage(BaseStorage):
    db_name = 'topic_store'

import sys
requests.settings.verbose = sys.stderr # TODO: point to logger stream
    
    
class BaseStorageTests(unittest.TestCase):
    def _make_one(self, *args, **kw):
        return BaseStorage(*args, **kw)
        
    def setUp(self):
        class TestRequests(object):
            def get(self, url, auth=None):
                return namedtuple('Response', 'content, status_code')(content=(url,auth), status_code=200)
                
            def put(self, url, auth=None, data=None):
                return namedtuple('Response', 'content, status_code')(content=(url,auth,data), status_code=201)
                
            def head(self, url, auth=None):
                return namedtuple('Response', 'headers, status_code')(headers={'Etag':url},status_code=200)

        
        global requests
        requests = TestRequests()
        
        config = {
                'server':'test_server',
                'username':'user',
                'password':'pass',
            }
        global load_config
        load_config = lambda : {'test_db': config}
        
        BaseStorage.db_name = 'test_db'
        
    def tearDown(self):
        import requests as requests_external
        global requests
        requests = requests_external
        
        import util
        global load_config
        load_config = util.load_config
        
        BaseStorage.db_name = None
        
    def test_handle_response(self):
        raise NotImplementedError
        
    def test_put_object(self):
        test_id = 'test_id'
        test_data = {'test_data':'test_value'}
        with self._make_one() as storage:
            url, auth, data = storage.put_object(test_id, test_data)
            self.assertEqual(url, 'test_server/test_db/'+test_id)
            self.assertEqual(auth, ('user','pass'))
            self.assertEqual(data, json.dumps(test_data))
        
    def test_get_object(self):
        with self._make_one() as storage:
            url, auth = storage.get_object('test_id')
            self.assertEqual(url, 'test_server/test_db/test_id')
            self.assertEqual(auth, ('user','pass'))
            
    def test_head_object_revision(self):
        with self._make_one() as storage:
            url = storage.head_object_revision('test_revision')
            self.assertEqual(url, 'test_server/test_db/test_revision')
        
    def test_get_view(self):
        test_param = {
                'test_key1':'test_value1',
                'test_key2':'test_value2',
            }
        with self._make_one() as storage:
            url, auth = storage._get_view('test_design', 'test_view', test_param)
            self.assertIn('test_server/_design/test_design/_view/test_view?', url)
            self.assertIn('test_key1=test_value1', url)
            self.assertIn('test_key2=test_value2', url)
            self.assertEqual(url.count('&'), 1)
            self.assertEqual(auth, ('user','pass'))
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BaseStorageTests))
    return suite
    
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())