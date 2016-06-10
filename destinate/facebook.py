import requests

HOST = 'https://graph.facebook.com/v2.5'
USER_FIELDS = 'fields=id,first_name,email,tagged_places{place{name,place_type,place_topics,location{city}}},events{name,description},location'

def get_user(token):
    try:
        data = get('me', USER_FIELDS, token)
    except requests.exceptions.HTTPError as error:
        if error.response.status_code == 400:
            print error.response.content
            raise ValueError
        raise
    return map_details(data)

def map_details(data):
    places = data.get('tagged_places',{}).get('data',[])
    events = data.get('events',{}).get('data',[])
    return {
        'facebook_id':data['id'],
        'name':data['first_name'],
        'email':data['email'],
        'city':map_place(data['location']) if 'location' in data else None,
        'places':[map_place(p['place']) for p in places if p['place'].get('location')],
        'events':[map_event(e) for e in events if 'description' in e]
        }
        
def map_place(data):
    place = {
        'name':data['name'],
        'city':data['location']['city'],
        }
    if data['place_type'] == 'PLACE' and data.get('place_topics',{}).get('data'):
        place['topics'] = [t['name'] for t in data['place_topics']['data']]
    return place
    
def map_event(data):
    return {
        'name':data['name'],
        'description':data['description'],
        }

def get(path, query, token):
    uri = '{}/{}?{}&access_token={}'.format(HOST,path,query,token)
    try:
        response = requests.get(uri)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print error.response.status_code, error.response.content
    return response.json()

