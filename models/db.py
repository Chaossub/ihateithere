from pymongo import MongoClient
from config import MONGODB_URI

# Initialize MongoDB client
mongo_client = MongoClient(MONGODB_URI, tls=True, tlsAllowInvalidCertificates=True, serverSelectionTimeoutMS=5000)

# Main bot database
db = mongo_client["succubot"]

# Collections
feds_col = db["federations"]
users_col = db["users"]
summon_col = db["summon"]
xp_col = db["xp"]
warns_col = db["warnings"]
