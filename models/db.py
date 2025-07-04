from pymongo import MongoClient
from config import MONGODB_URI

# Create Mongo client and connect to DB
mongo_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
succubot_db = mongo_client["succubot"]

# Collections
feds_col = succubot_db["federations"]
