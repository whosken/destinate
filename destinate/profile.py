import storage
import facebook
import nlp

import collections

from storage import get_user

def find_user(token):
    user = facebook.get_user(token)
    user['token'] = token
    user['summary'] = analyze_user(user)
    storage.upsert_user(user)
    return user
    
def analyze_user(user):
    topics = collections.Counter()
    cities = collections.Counter()
    for place in user.pop('places',[]):
        topics.update(place.get('topics') or [])
        cities[place['city']] += 1
    events = [nlp.translate(e['description']) for e in user.pop('events',[])]
    return {
        'cities':[c for c,_ in cities.most_common(5)],
        'topics':list(topics.elements()),
        'events':nlp.summarize(u'\n'.join(events), max_sentence_count=5)
        }

def is_valid_token(token, valid_minutes=360):
    return storage.login_user(token, valid_minutes) is not None
