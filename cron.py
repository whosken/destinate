import logging, unittest
from storage import PlaceStorage as Storage
from requestor import search_queries
from profiler import profile
import util

def run(rescrape=False, doc_list_name=None):
    store = Storage()
    docs = scrape(rescrape, doc_list_name)
    for doc_tuple in encode(docs):
        logging.info('Storing doc <{0}>'.format(doc_tuple[0]))
        response = store.put_place(doc_tuple)
        logging.info('Recieved resposne <{0}>'.format(response))

def scrape(rescrape=True, doc_list_name=None):
    if not rescrape: return None
    doc_ids = list(Storage().get_all_ids()) if not doc_list_name else util.iter_txt(doc_list_name)
    return search_queries(doc_ids)
    
def encode(doc_tuples=None):
    if not doc_tuples:
        def unpack_Place():
            for name, intro, body, profile in Storage().get_all_places():
                yield name, intro, body
        doc_tuples = unpack_Place()
    return profile(doc_tuples)
    
    
class CronTests(unittest.TestCase):
    def test_run(self):
        raise NotImplementedError

    def test_scape(self):
        raise NotImplementedError
        
    def test_encode(self):
        raise NotImplementedError
    
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CronTests))
    return suite
        
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())