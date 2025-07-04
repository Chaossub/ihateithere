import os
from dotenv import load_dotenv

load_dotenv()

# Telegram API credentials
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# MongoDB connection string
MONGODB_URI = (
    "mongodb+srv://chaossunflowerbusiness321:Sunflower@cluster0.y0defvi.mongodb.net/"
    "?retryWrites=true&w=majority&appName=Cluster0"
)

# Superusers (bot owner/admins with full access)
SUPERUSERS = [6964994611]
