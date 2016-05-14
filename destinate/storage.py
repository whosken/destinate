import elastic
import mongo

def upsert_cities(cities):
    elastic.create_index()
    actions = map(create_city_upsert, cities)
    elastic.helpers.bulk(elastic.client, actions)
    elastic.refresh_index()
    return True
    
def search_cities(query=None):
    return elastic.search(
        query,
        index=elastic.SEARCH_INDEX,
        path=[
            'city.name',
            'city.cid',
            'city.regions',
            'city.location'
            'city.images'
            ]
        )

def create_city_upsert(city):
    return {
        '_op_type':'update',
        '_id':city['cid'],
        '_index':elastic.SEARCH_INDEX,
        '_type':'city',
        'doc':city,
        'doc_as_upsert': True
        }
