import storage
import facebook
import nlp

import collections

get_user = storage.get_user_by_token # NOTE: for auth

def find_and_analyze_user(token):
    raw_user = facebook.get_user(token)
    user = storage.get_user_by_id(
        user_obj['facebook_id'],
        valid_days=30) # NOTE: force analysis every 30 days
    if not user:
        user = raw_user
        user['summary'] = analyze_user(user)
    user['token'] = token
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
        'cities':[c for c,_ in cities.most_common(10)],
        'topics':list(topics.elements()),
        'events':nlp.summarize(u'\n'.join(events), max_sentence_count=5)
        }
        
def remove_counter_long_tail(counter):
    ''' If the counter contains single occurence elements, remove the long tail '''
    try:
        if counter.most_common(1)[0][1] > 1:
            counter.subtract(list(counter))
    except IndexError:
        pass
    return counter

def is_valid_token(token, valid_minutes=360):
    return storage.get_user_by_token(
        token,
        valid_minutes,
        {'_id':True}) is not None
