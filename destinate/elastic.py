import elasticsearch
import elasticsearch.helpers as helpers
import elasticsearch.exceptions as exceptions

import os

HOST = os.environ.get('SEARCHBOX_URL')
SEARCH_INDEX = 'destinate'

class LazyClient(object):
    def __init__(self):
        self._client = False
        
    def __getattr__(self,name):
        if name == '_client':
            return self._client
        if not self._client:
            print 'connecting to', HOST
            if HOST:
                self._client = elasticsearch.Elasticsearch([HOST], port=80, timeout=30)
            else:
                self._client = elasticsearch.Elasticsearch(['localhost:9200'])
        return getattr(self._client, name)
    
client = LazyClient()

def delete_index(index=None):
    return client.indices.delete(index=index or SEARCH_INDEX, ignore=404)

def create_index(index=None):
    return client.indices.create(index=index or SEARCH_INDEX, ignore=400)

def refresh_index(index=None):
    return client.indices.refresh(index=index or SEARCH_INDEX)

PAGING_OPTIONS = ['fields', 'page', 'count', '_all']
def search(query=None, index=None, fields=None, page=0, count=10, _all=False):
    try:
        results = client.search(
            index=index or SEARCH_INDEX,
            body={'query': query or {'match_all':{}}},
            from_=page*count,
            size=count if not _all else 5000, # NOTE: there are roughly 4000+ cities with 100k+ population
            _source_include=fields
            )
    except exceptions.TransportError as error:
        print error.info
        raise
    total = results['hits'].get('total')
    print 'found', total
    return [h['_source'] for h in results['hits'].get('hits',[])]
