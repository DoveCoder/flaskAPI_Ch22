import pymongo
import json # parse to json
from bson import ObjectId # _id

# Connection string
# Allow connection to a database 
# url, etc needed for server

# mongo_url = "mongodb+srv://......." (example)

mongo_url = "mongodb://localhost:27017"

client = pymongo.MongoClient(mongo_url)

# Get or create the database
db = client.get_database("PenProfessional")

class JSONEncoder(json.JSONEncoder):
    def default(self, obj): # self(python) == this(javascript)
        if isinstance(obj, ObjectId): # equal to an object
            return str(obj)
        return JSONEncoder.default(obj)

def json_parse(data): # parse object into strings
    return JSONEncoder().encode(data)

