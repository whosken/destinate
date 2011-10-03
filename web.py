import logging, unittest
from flask import Flask
from suggestor import suggest
from storage import PlaceStorage as Storage
import json
import os

app = Flask(__name__)

@app.route('/suggest/place/<place_name>')
def get_similar_places(place_name):
    logging.info('Searching for place <{0}>'.format(place_name))
    return json.dumps(suggest(place_name))
    
@app.route('/info/place/<place_name>')
def get_place_info(place_name):
    logging.info('Getting place <{0}> info'.format(place_name))
    place = Storage().get_place(place_name)
    if place:
        name, info, body, _ = place
        return json.dumps({name:{'info':info,'body':body}})

if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0',port=port)