# FLASK SERVER
from flask import Flask
from flask_cors import CORS
from flask import request
from cerberus import Validator
import json
app = Flask(__name__)
CORS(app)


@app.route('/api/extension_post', methods=['GET', 'POST'])
def hello_world():
    schema = {'name': {'type': 'string'}}
    v = Validator()
    example = json.loads(request.data)
    print(v.validate(example, schema))
    if v.validate(example, schema):
        import pymongo
        client = pymongo.MongoClient(
            "mongodb+srv://projectcodeblue:1234@pcb-23.spovi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client["test_database"]
        collection = db["test_collection"]
        collection.insert_one(request.data)

    return


if __name__ == '__main__':
    # app.debug = True
    app.run(port=30009)
