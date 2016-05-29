import flask
import destinate
import destinate.storage
import destinate.facebook

app = flask.Flask(__name__)

def find_user():
    facebook_token = flask.request.form['facebook_token']
    preferred_months = flask.request.form.get('months')
    user = destinate.facebook.profile_user(facebook_token)
    destinate.storage.save_user(user)
    return user

@app.route('/suggestions/facebook/',methods=['POST'])
def suggest_from_facebook():
    user = find_user()
    suggestions = destinate.suggest_from_guide(user['preferences'])
    return flask.jsonify(suggestions=suggestions)

