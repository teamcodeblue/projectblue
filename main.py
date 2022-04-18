# FLASK SERVER
from cerberus import Validator
from flask import Flask
from flask_cors import CORS
from flask import request, Response
import json
from model.ContentBasedReccomendation.contentbasedrecommendation import reccomendations

app = Flask(__name__)
CORS(app)


@app.route('/api/extension_post', methods=['GET', 'POST'])
def hello_world():
    #print(request.data)
    import pymongo
    schema = {'url': {'type': 'string', 'empty': False}, 'timeSpend': {'type': 'float', 'empty': False}, 'html': {'type': 'string', 'empty': False}}
    v = Validator(schema)
    example = json.loads(request.data)
    if v.validate(example, schema):
        client = pymongo.MongoClient(
            "mongodb://127.0.0.1:27017/")
        db = client["test_database"]
        collection = db["test_collection"]
        collection.insert_one(example)

    return "a"


@app.route('/api/reccomendations_request', methods=['GET', 'POST'])
def post_reccomendations():
   stringy = {"text" : """2.2004077 Elon Musk says his offer to buy Twitter is about 'the future of civilization,' not making money
1.7853994 Apple store workers at Grand Central Terminal start collecting signatures to form a union
1.7619251 Bioengineering more efficient trees for carbon capture
1.4806573 GitHub Reportedly Suspends Accounts Related to Sanctioned Russian Orgs
""", "count": 4}

   return json.dumps(stringy)


if __name__ == '__main__':
    app.run(port=30009)
