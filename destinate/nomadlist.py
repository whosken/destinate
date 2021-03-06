import requests

API_HOST = u'https://nomadlist.com/api/v2'
PaGE_HOST = u'https://nomadlist.com'

def list_cities():
    return fetch()
    
def get_city(city_name):
    return fetch(name=city_name)

VALID_ACTIONS = ('list','filter')
VALID_SCOPES = ('cities','regions','countries')
def get_uri(action='list', scope='cities', name=None):
    if action not in VALID_ACTIONS or scope not in VALID_SCOPES:
        raise ValueError
    return u'{}/{}/{}/{}'.format(API_HOST, action, scope, name or '')

def fetch(*args, **kwargs):
    uri = get_uri(*args, **kwargs)
    print 'fetching', uri
    response = requests.get(uri)
    response.raise_for_status()
    data = response.json()
    return map(formats[data['type']], (data['result']))
    
def format_city(city):
    info = city['info']
    scores = city['scores']
    costs = city['cost']
    return {
        'cid': hash(info['city']['slug']),
        'name': info['city']['name'],
        'regions': [
            info['region']['name'],
            info['country']['name'],
            ],
        'location': info['location'],
        'weather': format_weather(info['weather']),
        'months_ideal': info['monthsToVisit'],
        'nomadlist':{
            'uri': '{}/{}'.format(PaGE_HOST, info['city']['slug']),
            'scores':{
                'nightlife': scores['nightlife'],
                'leisure': scores['leisure'],
                'air_condition': scores['aircon'],
                'safety': scores['safety'],
                'foreigner_friendly': scores['friendly_to_foreigners'],
                'racial_tolerance': scores['racism'],
                'lgbt_friendly': scores['lgbt_friendly'],
                'female_friendly': scores['female_friendly']
                },
            'costs':{
                'hotel': costs['hotel'],
                'airbnb': costs['airbnb_median'],
                'beer': costs['beer_in_cafe'],
                'coffee': costs['coffee_in_cafe']
                },
            }
        }
        
def format_weather(weather):
    return {
        'pattern': weather['type'],
        'humidity': weather['humidity']['value'],
        'temperature': weather['temperature']
        }

formats = {'cities':format_city}
