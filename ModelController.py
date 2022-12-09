# FLASK SERVER
from cerberus import Validator
from flask import Flask
from flask_cors import CORS
from flask import request, Response
import json
from model.ContentBasedReccomendation.model_defs import ArticleClassifier

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
    if True:  # v.validate(example, schema):
        client = pymongo.MongoClient(
            "mongodb://127.0.0.1:27017/")
        db = client["test_database"]
        collection = db["test_collection"]
        collection.insert_one({"url": example["url"], "html": example["html"]})
    return {"Status": "200"}


@app.route('/api/reccomendations_request', methods=['GET', 'POST'])
def post_reccomendations():


   ret_text = reccomendations(model_link="model/ContentBasedRecommendation/oldmodel.pt",Globals= Globals)
   stringy = {"text" :ret_text , "count": 4}

   return json.dumps(stringy)


'''
Contains functionality and 
abstraction of function calls 
to feed recent topics from the database
into the topic modeler
'''
import time

# Global Value for event callback
class Globals(object):
    PROGRESS = 0

# Main routine to begin maintence on topic modeler
def model_main():
    app.run(port=30009)

