import os
from pyrogram import Client
from pyrogram.enums import ParseMode
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize the bot client
app = Client(
    "SuccuBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode=ParseMode.HTML
)

# Import handlers (all decorated directly with @Client.on_message)
from handlers import (
    welcome,
    help_cmd,
    moderation,
    federation,
    summon,
    xp,
    fun
)

print("✅ SuccuBot is running...")
app.run()

