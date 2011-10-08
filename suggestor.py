import logging, unittest
from requestor import search_queries
from storage import PlaceStorage as Storage
from filter import score_candidates
from collections import Counter
import util

def suggest(target_name, count=20):
    logging.info('Suggesting locations for query: <{0}>'.format(target_name))
    storage = Storage()
    places = None

    doc_ids = list(storage.get_all_ids())
    if target_name in doc_ids:
        target_profile = storage.get_place(target_name).profile
    else:
        response = list(search_queries([target_name]))
        if len(response) > 0:
            name,info,body = response[0]
            target_profile = Counter(body.split())
            storage.put_object([name, info, body, target_profile])
        else: # target_text is not a place name, use binary place search
            target_profile = Counter(target_name.lower().split())
            places = storage.get_places_by_words(target_profile.iterkeys())
    if not places: places = storage.get_places(doc_ids)

    scored = score_candidates(target_profile, places)
    
    def filter_target():
        for index, (name, score) in enumerate(scored):
            if index >= count: break
            if name == target_name: continue
            yield name, score
        
    return zip(*filter_target())
    

class SuggestorTests(unittest.TestCase):
    def setUp(self):
        target_profile = {'test':6, 'case':4, 'unit':2, 'pass':1}
        profile_one = {'test':3, 'case':2, 'unit':1}
        profile_two = {'test':1, 'case':1, 'unit':1, 'fail':1}
        profile_three = {'fail':1}
        
        class TestPlace(object):
            def __init__(self, name, profile):
                self.name = name
                self.profile = profile
        
        class TestStorage(object):
            def get_place(self, target_name):
                return TestPlace('test_profile',target_profile)
                
            def get_all_ids(self):
                return 'one', 'two', 'three'
                
            def get_places_by_words(self, places):
                return [
                        TestPlace('one',profile_one),
                        TestPlace('two',profile_two),
                        TestPlace('three',profile_three),
                    ]
                    
            def get_all_places(self):
                return [
                        TestPlace('one',profile_one),
                        TestPlace('two',profile_two),
                        TestPlace('three',profile_three),
                    ]
                    
        global Storage
        Storage = TestStorage
        global search_queries
        search_queries = lambda x: []
        
    def tearDown(self):
        from storage import PlaceStorage
        global Storage
        Storage = PlaceStorage
        from requestor import search_queries as search
        global search_queries
        search_queries = search
        
    def test_suggest(self):
        ranked_names, ranked_scores = suggest('one')
        self.assertEqual(' '.join(ranked_names), 'two three')
        for i, score in enumerate(ranked_scores):
            if i+1 >= len(ranked_names): break
            self.assertTrue(score > ranked_scores[i+1])
    
    def test_suggest(self):
        ranked_names, ranked_scores = suggest('test case unit pass')
        self.assertEqual(' '.join(ranked_names), 'one two three')
        for i, score in enumerate(ranked_scores):
            if i+1 >= len(ranked_names): break
            self.assertTrue(score > ranked_scores[i+1])    
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SuggestorTests))
    return suite
        
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())