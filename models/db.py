from pymongo import MongoClient
import certifi
from config import MONGODB_URI

mongo_client = MongoClient(MONGODB_URI, tlsCAFile=certifi.where())
succubot_db = mongo_client["succubot"]

# Collections:
feds_col = succubot_db["federations"]
