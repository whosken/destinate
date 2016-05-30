import requests

HOST = 'https://graph.facebook.com/v2.5'
USER_FIELDS = 'fields=id,first_name,email,checkins,city'
PLACE_FIELDS = 'fields='

def get_user(token):
    data = get('me', USER_FIELDS, token)
    return map_details(data)
    
def get_place(place_id, token):
    data = get(place_id, PLACE_FIELDS, token)
    pass

def map_details(data):
    return {
        'facebook_id':data['id'],
        'name':data['first_name'],
        'email':data['email'],
        'city':data['city'], # TODO: verify
        'places':map(map_checkin, data['checkins']) # TODO: verify
        }
        
def map_checkin(data):
    pass

def get(path, query, token):
    uri = '{}/{}?{}&access_token={}'.format(HOST,path,query,token)
    try:
        response = requests.get(uri)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print error.response.content
    return response.json()

