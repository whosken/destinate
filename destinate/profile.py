import storage
import facebook
import nlp

def find_user(token):
    user = destinate.facebook.get_user(token)
    user['token'] = token
    user['summary'] = analyze_user(user, token)
    destinate.storage.upsert_user(user)
    return user
    
def analyze_user(user):
    pass

def get_user(token):
    return storage.get_user(token)

def is_valid_token(token, valid_minutes=90):
    user = storage.get_user(token, valid_minutes, fields={'_id':True})
    return bool(user)
    