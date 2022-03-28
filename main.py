#FLASK SERVER
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/extension_post')
def hello_world():
   import pymongo

   client = pymongo.MongoClient(
      "mongodb+srv://projectcodeblue:1234@pcb-23.spovi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
   db = client["test_database"]

   collection = db["test_collection"]

   example = {"id": 0, "Body": {"url": "www.nike.com", "content": "Sports Wear"}}

   collection.insert_one(example)
   return

if __name__ == '__main__':
   app.run(port=30009)