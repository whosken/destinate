import logging, unittest
from requestor import search_queries
from storage import PlaceStorage as Storage
from filter import score_candidates
from collections import Counter
import util

def suggest(target_name, count=20):
    storage = Storage()

    doc_ids = list(storage.get_all_ids())
    if target_name in doc_ids:
        target_profile = storage.get_place(target_name).profile
    else:
        name,info,body = search_queries([target_name], doc_ids)
        target_profile = Counter(body.split())
        storage.put_object([name, info, body, target_profile])
    
    scored = score_candidates(target_profile, storage.get_all_places())
    
    def filter_target():
        for index, (name, score) in enumerate(scored):
            if index == count: break
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
                
            def get_all_places(self):   
                return [
                        TestPlace('one',profile_one),
                        TestPlace('two',profile_two),
                        TestPlace('three',profile_three),
                    ]
                    
        global Storage
        Storage = TestStorage
        
    def tearDown(self):
        from storage import PlaceStorage
        global Storage
        Storage = PlaceStorage
        
    def test_suggest(self):
        ranked_names, ranked_scores = suggest('one')
        self.assertEqual(' '.join(ranked_names), 'two three')
        for i, score in enumerate(ranked_scores):
            if i+1 >= len(ranked_names): break
            self.assertTrue(score > ranked_scores[i+1])
            
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SuggestorTests))
    return suite
        
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())