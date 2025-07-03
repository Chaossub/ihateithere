from pymongo import MongoClient
from config import MONGODB_URI

mongo_client = MongoClient(
    MONGODB_URI,
    tls=True,
    tlsAllowInvalidCertificates=False  # or True only if you absolutely trust the certs
)

succubot_db = mongo_client["succubot"]

# Collections:
feds_col = succubot_db["federations"]
