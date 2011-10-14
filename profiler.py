import logging, unittest
from math import log
from util import load_config
from collections import Counter

def profile(doc_tuples):
    profiler = TfIdfProfiler()
    logging.info('Starting doc profiling')
    return profiler.profile(doc_tuples)

class TfIdfProfiler(object):
    """
    Profile each document as tf-idf scores
    """
    
    def profile(self, iter_docs):
        doc_tuples = list(iter_docs)
        profiles, corpus = self._calculate_tf(doc_tuples)
        profiles = self._apply_idf(profiles, corpus)
        for name, intro, body in doc_tuples:
            yield name, intro, body, profiles[name]
        
    def _apply_idf(self, profiles, corpus, sparse=True):
        sparse_factor = 1 if not sparse else load_config()['encode_factor']
        profiles_count = len(profiles)
        
        def calculate_score(tf_tuple):
            term, tf = tf_tuple
            idf = profiles_count / corpus[term]
            if idf < 0: return term, 0
            tf_idf = tf * log(idf)
            return term, tf_idf
            
        def calculate_profile(profile_tuple):
            name, profile = profile_tuple
            limit = int(len(profile)/sparse_factor)
            tf_idf_tuples = map(calculate_score, profile.iteritems())
            top_terms = Counter(dict(tf_idf_tuples)).most_common()[:limit]
            return name, dict(top_terms)
        
        logging.info('Starting IDF profiling')
        profiles_list = map(calculate_profile,profiles.iteritems())
        return dict(profiles_list)
        
    def _calculate_tf(self, doc_tuples):
        corpus = Counter()
        profiles = {}
        
        def yield_words(body):
            for word in body.lower().split():
                try:
                    float(word)
                except ValueError:
                    yield word
        
        logging.info('Starting TF profiling')
        for name, intro, body in doc_tuples:
            bag = Counter(yield_words(body))
            profiles[name] = bag
            corpus.update(bag.iterkeys())
        return profiles, corpus
        

class TfIdfProfilerTests(unittest.TestCase):
    def _make_one(self, *args, **kw):
        return TfIdfProfiler(*args, **kw)
        
    def setUp(self):
        global load_config
        load_config = lambda : {'encode_factor': 1}
        
    def tearDown(self):
        import util
        global load_config
        load_config = util.load_config
        
    def test_calculate_tf(self):
        profile_one = ('one',None,'test case test case test unit')
        profile_two = ('two',None,'test case test case test unit')
        docs = [profile_one, profile_two]
        
        profiler = self._make_one()
        profiles, corpus = profiler._calculate_tf(docs)
        self.assertEqual(profiles['one']['test'], 3)
        self.assertEqual(profiles['one']['case'], 2)
        self.assertEqual(profiles['one']['unit'], 1)
        self.assertEqual(corpus['test'], 2)
        self.assertEqual(corpus['case'], 2)
        self.assertEqual(corpus['unit'], 2)
        
    def test_apply_idf(self):
        profiles = {'one':Counter('test case test case test unit'.split())}
        corpus = Counter(profiles['one'].keys())
        
        profiler = self._make_one()
        result = dict(profiler._apply_idf(profiles, corpus)['one'])
        self.assertEqual(result['test'], 0)
        self.assertEqual(result['case'], 0)
        self.assertEqual(result['unit'], 0)
        
        profiles.update({'two':Counter('unit'.split())})
        corpus.update(profiles['two'].keys())
        
        result = dict(profiler._apply_idf(profiles, corpus)['one'])
        self.assertTrue(result['test'] > 0)
        self.assertTrue(result['case'] > 0)
        self.assertEqual(result['unit'], 0)
        
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TfIdfProfilerTests))
    return suite
    
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())