import flask
import destinate

app = flask.Flask(__name__)

@app.route('/suggestions/facebook/',methods=['POST'])
def suggest_from_facebook():
    user = destinate.profile.find_user(
        flask.request.form['facebook_token'],
        months=flask.request.form.get('months')
        )
    suggestions = destinate.suggest.from_guide(
        user['summary'],
        months=user['months']
        )
    return flask.jsonify(suggestions=suggestions)
