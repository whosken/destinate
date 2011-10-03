import logging, unittest
from operator import mul, itemgetter
from math import sqrt

def score_candidates(target_profile, candidates):
    filter = CosSimFilter()
    scored = filter.score_candidates(target_profile, candidates)
    return sorted(list(scored),key=itemgetter(1), reverse=True)

class CosSimFilter(object):
    """
    Ranks a list of candidates by cos-sim distance to a target
    """
    
    def score_candidates(self, target_profile, candidates):
        for candidate in candidates:
            _, a, b = self._create_vectors(target_profile, candidate.profile)
            yield candidate.name, self._calculate_score(a,b)
    
    def _calculate_score(self, a, b):
        def dot(*vectors):
            return sum(map(mul,*vectors))
        
        def magnitude(vector):
            return sqrt(dot(vector, vector))
            
        return dot(a, b) / magnitude(a) / magnitude(b)
        
    def _create_vectors(self, target, profile):
        def yield_vectors():
            for key in (set(target) | set(profile)):
                yield key, target.get(key, 0), profile.get(key, 0)
        
        return zip(*yield_vectors())
        
    
class CosSimFilterTests(unittest.TestCase):
    def _make_one(self, *args, **kw):
        return CosSimFilter(*args, **kw)
        
    def setUp(self):
        from collections import Counter
        self.target = Counter({'test':6, 'case':4, 'unit':2, 'pass':1})
        profile_one = Counter({'test':3, 'case':2, 'unit':1})
        profile_two = Counter({'test':1, 'case':1, 'unit':1, 'fail':1})
        profile_three = Counter({'fail':1})
        
        class TestProfile(object):
            def __init__(self, name, profile):
                self.name = name
                self.profile = profile
        
        self.test_profiles = [
                TestProfile('one',profile_one),
                TestProfile('two',profile_two),
                TestProfile('three',profile_three),
            ]
        
    def tearDown(self):
        pass
        
    def test_score_candidates(self):
        filter = self._make_one()
        ranked_list = filter.score_candidates(self.target, self.test_profiles)
        ranked_names, ranked_scores = zip(*ranked_list)
        self.assertEqual(' '.join(ranked_names), 'one two three')
        for i, score in enumerate(ranked_scores):
            if i+1 >= len(ranked_scores): break
            self.assertTrue(score > ranked_scores[i+1])
        
    def test_calculate_score(self):
        filter = self._make_one()
        target_vector = [2,2,2,2,0]
        profile_vector = [1,1,1,0,1]
        score = filter._calculate_score(target_vector, profile_vector)
        self.assertEqual(score, .75) # = A dot B / |A||B| = 6 / 4 / 2 = 3 / 4
        
    def test_create_vectors(self):
        filter = self._make_one()
        test_profile = self.test_profiles[1].profile
        keys, target_vector, profile_vector = filter._create_vectors(self.target, test_profile)
        self.assertEqual(len(set(keys) - set('test case unit pass fail'.split())), 0)
        for i, key in enumerate(keys):
            self.assertEqual(self.target[key], target_vector[i])
            self.assertEqual(test_profile[key], profile_vector[i])
    
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CosSimFilterTests))
    return suite
    
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())