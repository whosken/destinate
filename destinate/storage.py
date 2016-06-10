import elastic
import mongo
import datetimeutc

from elastic import PAGING_OPTIONS

def upsert_user(user):
    query = {'_id':hash(user['facebook_id'])}
    update = {
        '$set':user,
        '$currentDate':{'last_login':True},
        }
    mongo.db.users.update_one(query, update, upsert=True)
    return True
    
def login_user(token, valid_minutes=360):
    then = datetimeutc.Datetime.now() - datetime.timedelta(minutes=valid_minutes)
    query = {
        'token':token,
        'last_login':{'$gte':then}
        }
    update = {'currentDate':{'last_login':True}}
    return mongo.db.users.find_one_and_update(query, update, {'_id':True})
    
def get_user(token, fields=None):
    return mongo.db.users.find_one({'token':token}, fields)

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
