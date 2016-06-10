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
    topics = remove_counter_long_tail(topics)
    events = [nlp.translate(e['description']) for e in user.pop('events',[])]
    return {
        'cities':[c for c,_ in cities.most_common(5)],
        'topics':list(topics.elements()),
        'events':nlp.summarize(u'\n'.join(events), max_sentence_count=5)
        }
        
def remove_counter_long_tail(counter):
    try:
        if counter.most_common(1)[0][1] > 1:
            counter.subtract(list(counter)) # removes the long tail
    except IndexError:
        pass
    return counter

def is_valid_token(token, valid_minutes=360):
    return storage.get_user(token, valid_minutes, {'_id':True}) is not None
