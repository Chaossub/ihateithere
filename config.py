import os
from dotenv import load_dotenv

load_dotenv()

# Telegram API credentials
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# MongoDB URI (with correct format)
MONGODB_URI = "mongodb+srv://chaossunflowerbusiness321:Urmom420@cluster0.y0defvi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Superusers (Telegram user IDs that have full control)
SUPERUSERS = [6964994611]  # ← Your Telegram ID


