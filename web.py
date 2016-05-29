import flask
import destinate
import destinate.storage
import destinate.facebook

app = flask.Flask(__name__)

def find_user():
    facebook_token = flask.request.form['facebook_token']
    user = destinate.facebook.profile_user(facebook_token)
    destinate.storage.upsert_user(user)
    return user

@app.route('/suggestions/facebook/',methods=['POST'])
def suggest_from_facebook():
    user = find_user()
    preferred_months = flask.request.form.get('months')
    suggestions = destinate.suggest_from_guide(
        user['preferences'],
        months=preferred_months
        )
    return flask.jsonify(suggestions=suggestions)
