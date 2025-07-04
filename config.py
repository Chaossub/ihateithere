import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Your Telegram user ID (superuser)
SUPERUSERS = [6964994611]

# Updated, secure MongoDB connection string
MONGODB_URI = "mongodb+srv://chaossunflowerbusiness321:Urmom420@cluster0.y0defvi.mongodb.net/succubot?retryWrites=true&w=majority&tls=true"

