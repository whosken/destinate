import logging, unittest
from storage import PlaceStorage as Storage
from requestor import search_queries
from profiler import profile
import util

def run(rescrape=False, doc_list_name=None):
    store = Storage()
    docs = scrape(store, rescrape, doc_list_name)
    doc_tuples = profile(docs)
    list(store.put_places(doc_tuples))
    store.compact()
    
def scrape(store, rescrape, doc_list_name):
    doc_ids = store.get_all_ids() if not doc_list_name else util.iter_txt(doc_list_name)
    
    if rescrape:
        return search_queries(doc_ids)
        
    def get_places():
        for name, intro, body, _ in store.get_places(doc_ids):
            yield name,intro,body
    return get_places()
    
    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Parser for Cron')
    parser.add_argument('--rescrape', '-r', default=False, dest='rescrape', action='store_true', help='Scrape from Data Source')
    parser.add_argument('place_list', default=None, nargs='?', type=str, help='List of Places')
    args = parser.parse_args()
    run(args.rescrape, args.place_list)