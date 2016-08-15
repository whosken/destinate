import storage
import facebook
import nlp

import collections

get_user = storage.get_user_by_token # NOTE: for auth

def find_user(token, force_analyze=False): # NOTE: offload analyze_user to background?
    user = facebook.get_user(token)
    if not force_analyze:
        storaged_user = storage.get_user_by_id(user['facebook_id'])
        if storaged_user:
            return storaged_user
    print 'analyze user', user['email'].encode('utf8')
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
    return storage.get_user_by_token(token, valid_minutes, {'_id':True}) is not None
