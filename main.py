import os
from pyrogram import Client
from pyrogram.enums import ParseMode

from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "SuccuBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode=ParseMode.HTML
)

# Import handlers
from handlers import (
    moderation,
    federation,
    summon,
    fun,
    welcome,
    help_cmd
)

# Register handlers
moderation.register(app)
federation.register(app)
summon.register(app)
fun.register(app)
welcome.register(app)
help_cmd.register(app)

print("✅ SuccuBot is running...")
app.run()

