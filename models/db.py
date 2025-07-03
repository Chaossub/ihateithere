from pymongo import MongoClient
from config import MONGODB_URI

mongo_client = MongoClient(MONGODB_URI)
succubot_db = mongo_client["succubot"]

# Collections:
feds_col = succubot_db["federations"]
