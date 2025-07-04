import json
from functools import wraps
from pyrogram.types import ChatPermissions
from datetime import datetime, timedelta

# Admin-only decorator
def admin_only(func):
    @wraps(func)
    async def wrapper(client, message):
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status in ("administrator", "creator"):
            return await func(client, message)
        return await message.reply("🚫 You need to be an admin to use this command.")
    return wrapper

# Mute user
async def mute(client, chat_id, user_id, duration_seconds=None):
    try:
        until_date = None
        if duration_seconds:
            until_date = datetime.utcnow() + timedelta(seconds=duration_seconds)

        permissions = ChatPermissions(
            can_send_messages=False
        )
        await client.restrict_chat_member(chat_id, user_id, permissions, until_date=until_date)
        return True
    except Exception as e:
        print(f"Failed to mute: {e}")
        return False

# Unmute user
async def unmute(client, chat_id, user_id):
    try:
        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
        await client.restrict_chat_member(chat_id, user_id, permissions)
        return True
    except Exception as e:
        print(f"Failed to unmute: {e}")
        return False

# Warning system
def load_warns():
    try:
        with open("warns.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_warns(warns):
    with open("warns.json", "w") as f:
        json.dump(warns, f, indent=2)

def get_warns(user_id):
    warns = load_warns()
    return warns.get(str(user_id), 0)

def add_warn(user_id):
    warns = load_warns()
    warns[str(user_id)] = warns.get(str(user_id), 0) + 1
    save_warns(warns)
    return warns[str(user_id)]

def reset_warns(user_id):
    warns = load_warns()
    warns[str(user_id)] = 0
    save_warns(warns)

