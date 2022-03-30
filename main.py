#FLASK SERVER
from flask import Flask
from flask_cors import CORS
from flask import request

app = Flask(__name__)
CORS(app)


@app.route('/api/extension_post',methods = ['GET', 'POST'])
def hello_world():
   print(request.data)
   import pymongo

   client = pymongo.MongoClient(
      "mongodb+srv://projectcodeblue:1234@pcb-23.spovi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
   db = client["test_database"]

   collection = db["test_collection"]

   example = {request.data}

   collection.insert_one(example)
   return

if __name__ == '__main__':
   app.run(port=30009)


