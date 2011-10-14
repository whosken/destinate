import logging, unittest
from storage import PlaceStorage as Storage
from requestor import search_queries
from profiler import profile

def run(rescrape=False, from_list=None):
    store = Storage()
    docs = scrape(store, rescrape, from_list)
    doc_tuples = profile(docs)
    list(store.put_places(doc_tuples))
    store.compact()
    
def scrape(store, rescrape, from_list):
    if not (from_list and rescrape):
        doc_ids = store.get_all_ids()
    else:
        from util import iter_txt, load_config
        doc_ids = iter_txt(load_config()['place_list'])
    
    if rescrape:
        for name,intro,body in search_queries(doc_ids):
            store.put_place((name,intro,body,''))
            yield name,intro,body
    else:
        for name, intro, body, _ in store.get_places(doc_ids):
            yield name,intro,body
    
    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Parser for Cron')
    parser.add_argument('--rescrape', '-r', default=False, dest='rescrape', action='store_true', help='Scrape from Data Source')
    parser.add_argument('--from_list', '-l', default=False, dest='from_list', action='store_true', help='Use List of Places defined in yaml')
    args = parser.parse_args()
    run(args.rescrape, args.from_list)