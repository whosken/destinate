import storage
import facebook
import nlp

def find_user(token, months=None):
    user = {
        'facebook_token':token,
        'months':months
        }
    facebook_data = destinate.facebook.get_user(token)
    user.update(facebook_data)
    user['summary'] = analyze_user(user, token)
    destinate.storage.upsert_user(user)
    return user
    
def analyze_user(user):
    pass
