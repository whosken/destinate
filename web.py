import flask
import destinate

import os

SECRET = os.environ.get('SERVER_SECRET') or 'default_secret_key'
SESSION_TOKEN = 'user-session-token'

app = flask.Flask(__name__)
app.secret_key = SECRET
app.debug=True

def auth(func):
    def auth_and_run(*args, **kwargs):
        token = flask.session.get(SESSION_TOKEN)
        if token and authenticate(token):
            return func(*args, **kwargs)
        return flask.abort(403)
    return auth_and_run
    
def authenticate(token):
    return destinate.profile.is_valid_token(token)

@app.route('/logins/',methods=['POST'])
def login():
    token = flask.request.form['token']
    try:
        user = destinate.profile.find_user(token)
    except ValueError:
        return flask.abort(400)
    response = flask.make_response(flask.jsonify(user=user))
    flask.session[SESSION_TOKEN] = token
    return response

@app.route('/suggestions/')
@auth
def suggest():
    user = destinate.profile.get_user(flask.session[SESSION_TOKEN])
    cities = destinate.suggest.from_cities(
        months=flask.request.form.get('months'),
        ignore_name=user.get('city')
        *user['summary']['cities'])
    return flask.jsonify(suggestions=cities)
