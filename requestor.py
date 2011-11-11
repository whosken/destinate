import requests
import logging, unittest
import re

def search_queries(queries, language='en'):
    requestor = WikiTravelRequestor()
    logging.info('Starting place requesting')
    for query in queries:
        place_tuple = requestor.search_query(query)
        if place_tuple: yield place_tuple

class WikiTravelRequestor(object):
    """
    A request class that requests and parses WikiTravel pages
    """
    
    base_url = 'http://wikitravel.org'
    
    def search_query(self, query, language='en'):
        """
        Entry function that takes a query term and return a parsed tuple with name, info, and body values
        """
        logging.info('Requesting WikiTravel for query <{0}>'.format(repr(query)))
        response = self._fetch_page(query.strip().title().replace(' ','_'), language)
        logging.info('Parsing WikiTravel result for query <{0}>'.format(repr(query)))
        return self._parse_page_to_place(response.content)
    
    def _fetch_page(self, query, language):
        url = '/'.join((self.base_url,language,query))
        return requests.get(url)
    
    def _parse_page_to_place(self, page):
        def clean_string(string):
            new_string = re.sub(r'<[^<]*?>|\W', ' ', string)
            return re.sub(r'\s+', ' ', new_string)
        
        try:
            name = re.search(r'<h1[^>]*>(.*)</h1>', page).group(1)
            body = re.search(r'<p>([\s\S]*)</p>', page).group(1)
        except AttributeError, e:
            logging.error('Received error <{0}> while parsing WikiTravel'.format(repr(e)))
            return
        body = clean_string(body)
        intro = body[:500 if len(body) >= 500 else len(body)]
        return name, intro, body

        
import sys
requests.settings.verbose = sys.stderr # TODO: point to logger stream

        
class WikiTravelRequestorTests(unittest.TestCase):
    def _make_one(self, *args, **kw):
        return WikiTravelRequestor(*args, **kw)
        
    def setUp(self):
        from collections import namedtuple
        class TestRequests(object):
            def get(self, url, auth=None):
                return namedtuple('Response', 'content')(content=url)
        
        global requests
        requests = TestRequests()
        
    def tearDown(self):
        import requests as requests_external
        global requests
        requests = requests_external
    
    def test_fetch_page(self):
        query = 'test_query'
        language = 'en'
        requestor = self._make_one()
        url = requestor._fetch_page(query, language).content
        self.assertTrue('http://wikitravel.org/' + language + '/' + query in url)
    
    def test_page_parser(self):
        page = """
            <h1 class="firstHeading">test_page</h1>
            <p>test_intro</p>
            <p>test_intro2</p>
            <a name="Regions" />
            <p>test_content1</p>
            <a name="Understanding" />
            <p>test_content2</p>"""
            
        requestor = self._make_one()
        name, intro, body = requestor._parse_page_to_place(page)
        self.assertEqual(name, 'test_page')
        self.assertIn('test_intro', body)
        self.assertIn('test_intro2', body)
        self.assertIn('test_content1', body)
        self.assertIn('test_content2', body)
        self.assertIn('test_intro', intro)
        self.assertIn('test_intro2', intro)
        self.assertIn('test_content1', intro)
        self.assertIn('test_content2', intro)
        
    def test_page_parser_handles_empty_page(self):
        requestor = self._make_one()
        place = requestor._parse_page_to_place('')
        self.assertEqual(place, None)
    
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(WikiTravelRequestorTests))
    return suite
        
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())