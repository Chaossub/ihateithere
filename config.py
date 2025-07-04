import os
from dotenv import load_dotenv

load_dotenv()  # Only needed if testing locally

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGODB_URI = os.getenv("MONGODB_URI")  # Set this in Railway secrets

# Optional fallback
if not MONGODB_URI:
    raise Exception("❌ MONGODB_URI not found in environment variables.")
