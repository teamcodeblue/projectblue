# FLASK SERVER
from cerberus import Validator
from flask import Flask
from flask_cors import CORS
from flask import request, Response
import json
from model.ContentBasedReccomendation.model_defs import ArticleClassifier
cache_run_time = 30
from model.ContentBasedReccomendation.contentbasedrecommendation import reccomendations, Cache_result
Last_Ran = None
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
    import time
    if Last_Ran and Cache_result and Last_Ran + cache_run_time >= time.time():
        stringy = {"text": Cache_result, "count": 4}
        return json.dumps(stringy)
    else:
        Last_Ran =  time.time()
        ret_text = reccomendations(model_link="model/ContentBasedRecommendation/oldmodel.pt")
        stringy = {"text" :ret_text , "count": 4}


@app.route('/api/force_reccomendations_request', methods=['GET', 'POST'])
def force_reccomendations():
   ret_text = reccomendations(model_link="model/ContentBasedRecommendation/oldmodel.pt")
   stringy = {"text" :ret_text , "count": 4}

   return json.dumps(stringy)
if __name__ == '__main__':
    app.run(port=30009)


