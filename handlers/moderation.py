import json
import os
from pyrogram import filters
from pyrogram.types import Message
from handlers.utils import admin_only, mute, unmute, get_warns, add_warn, reset_warns, save_warns

WARN_FILE = "data/warnings.json"
os.makedirs("data", exist_ok=True)

def load_warns():
    if not os.path.isfile(WARN_FILE):
        return {}
    with open(WARN_FILE, "r") as f:
        return json.load(f)

warn_data = load_warns()

def register(app):

    @app.on_message(filters.command("warn") & filters.group)
    @admin_only
    async def warn_user(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user to warn them.")
            return

        user_id = str(message.reply_to_message.from_user.id)
        chat_id = str(message.chat.id)

