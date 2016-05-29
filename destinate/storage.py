import elastic
import mongo

def upsert_user(user):
    pass

def upsert_cities(cities, reset=False):
    if reset:
        elastic.delete_index()
    elastic.create_index()
    actions = map(create_city_upsert, cities)
    elastic.helpers.bulk(elastic.client, actions)
    elastic.refresh_index()
    return True
    
def search_cities(query=None, **options):
    if 'fields' not in options:
        options['fields'] = [
            'name',
            'cid',
            'regions',
            'location',
            'images'
            ]
    return elastic.search(
        query,
        index=elastic.SEARCH_INDEX,
        **options)

def create_city_upsert(city):
    return {
        '_op_type':'update',
        '_id':hash(city['cid']),
        '_index':elastic.SEARCH_INDEX,
        '_type':'city',
        'doc':city,
        'doc_as_upsert': True
        }
