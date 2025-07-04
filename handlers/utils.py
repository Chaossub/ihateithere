import json
import os
from functools import wraps
from pyrogram import filters
from pyrogram.types import Message, ChatPermissions
from datetime import datetime, timedelta
from config import SUPERUSERS

WARN_FILE = "data/warns.json"

def load_warns():
    if not os.path.exists(WARN_FILE):
        return {}
    with open(WARN_FILE, "r") as f:
        return json.load(f)

def save_warns(warns):
    with open(WARN_FILE, "w") as f:
        json.dump(warns, f, indent=2)

def get_warns(user_id, chat_id):
    warns = load_warns()
    return warns.get(str(chat_id), {}).get(str(user_id), 0)

def add_warn(user_id, chat_id):
    warns = load_warns()
    warns.setdefault(str(chat_id), {})[str(user_id)] = get_warns(user_id, chat_id) + 1
    save_warns(warns)
    return warns[str(chat_id)][str(user_id)]

def reset_warns(user_id, chat_id):
    warns = load_warns()
    if str(chat_id) in warns and str(user_id) in warns[str(chat_id)]:
        del warns[str(chat_id)][str(user_id)]
        save_warns(warns)

# Decorator: Only admins or SUPERUSERS
def admin_only(func):
    @wraps(func)
    async def wrapper(client, message: Message):
        user = message.from_user
        chat = message.chat
        if user.id in SUPERUSERS:
            return await func(client, message)
        member = await client.get_chat_member(chat.id, user.id)
        if member.status in ["administrator", "creator"]:
            return await func(client, message)
        await message.reply("❌ You must be an admin to use this command.")
    return wrapper

# Check if a user is admin or owner
async def is_admin_or_owner(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except:
        return False

# Mute a user
async def mute(client, chat_id, user_id, duration, message):
    try:
        until_date = int((datetime.utcnow() + timedelta(minutes=duration)).timestamp()) if duration else None
        await client.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(),
            until_date=until_date
        )
        await message.reply(f"🔇 User muted {'for ' + str(duration) + ' minutes' if duration else 'indefinitely'}.")
    except Exception as e:
        await message.reply(f"Failed to mute: <code>{e}</code>")

# Unmute a user
async def unmute(client, chat_id, user_id, message):
    try:
        await client.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await message.reply("🔊 User has been unmuted.")
    except Exception as e:
        await message.reply(f"Failed to unmute: <code>{e}</code>")
