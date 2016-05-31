import flask
import destinate

import os

SECRET = os.environ.get('SERVER_SECRET')
SESSION_TOKEN = 'user-session-token'

app = flask.Flask(__name__)
# use secret for hashing session headers

def auth(func):
    def auth_and_run(*args, **kwargs):
        token = flask.request.session.get(SESSION_TOKEN)
        if token and authenticate(token):
            return func(*args, **kwargs)
        return flask.abort(403)
    return auth_and_run
    
def authenticate(token):
    return destinate.profile.is_valid_token(token)

@app.route('/logins/',methods=['POST'])
def login():
    token = flask.request.form['token']
    user = destinate.profile.find_user(token)
    response = flask.make_response(flask.jsonify(user=user))
    response.session[SESSION_TOKEN] = token
    return response

@app.route('/suggestions/')
@auth
def suggest():
    cities = destinate.suggest.from_guide(
        user['summary'],
        months=flask.request.form.get('months')
        )
    return flask.jsonify(suggestions=cities)
