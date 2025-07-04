import os
from pyrogram import Client
from pyrogram.enums import ParseMode
from dotenv import load_dotenv

# Load environment variables from .env if available
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

# Import all handlers so their decorators register commands
from handlers import (
    welcome,
    help_cmd,
    moderation,
    federation,
    summon,
    xp,
    fun
)

# Register all handlers (if handlers use function-based registration, call .register(app))
welcome
help_cmd
moderation
federation
summon
xp
fun

print("✅ SuccuBot is running...")
app.run()

