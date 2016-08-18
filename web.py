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
    
def enable_jsonp_response(*args, **kwargs):
    callback = flask.request.args.get('callback')
    json_str = flask.json.dumps(*args, **kwargs)
    if callback:
        json_str = '{}({});'.format(callback, json_str)
    response = flask.make_response(json_str)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/logins/',methods=['POST'])
def login():
    token = flask.request.form['token']
    try:
        user = destinate.profile.find_and_analyze_user(token)
    except ValueError:
        return flask.abort(400)
    response = enable_jsonp_response(user=user)
    flask.session[SESSION_TOKEN] = token
    return response

@app.route('/suggestions/')
@auth
def suggest():
    user = destinate.profile.get_user(flask.session[SESSION_TOKEN])
    months=flask.request.values.getlist('month')
    regions=flask.request.values.getlist('region')

    guide = user['summary']['events'] + '\n' + u', '.join(user['summary']['topics'])
    cities = destinate.suggest.from_guide(
        guide,
        months=months,
        ignore_name=user.get('city'))
    return enable_jsonp_response(suggestions=cities)
    