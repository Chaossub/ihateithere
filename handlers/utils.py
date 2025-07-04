import json
import os
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatPermissions
from functools import wraps
from datetime import datetime, timedelta
import asyncio

WARN_FILE = "data/warnings.json"

def load_warns():
    if not os.path.exists(WARN_FILE):
        return {}
    with open(WARN_FILE, "r") as f:
        return json.load(f)

def save_warns(warns):
    with open(WARN_FILE, "w") as f:
        json.dump(warns, f, indent=2)

def get_warns(chat_id, user_id):
    warns = load_warns()
    return warns.get(str(chat_id), {}).get(str(user_id), 0)

def add_warn(chat_id, user_id):
    warns = load_warns()
    chat_str, user_str = str(chat_id), str(user_id)
    warns.setdefault(chat_str, {})[user_str] = warns.get(chat_str, {}).get(user_str, 0) + 1
    save_warns(warns)
    return warns[chat_str][user_str]

def reset_warns(chat_id, user_id):
    warns = load_warns()
    if str(chat_id) in warns and str(user_id) in warns[str(chat_id)]:
        warns[str(chat_id)][str(user_id)] = 0
    save_warns(warns)

def admin_only(func):
    @wraps(func)
    async def wrapper(client, message):
        try:
            user_id = message.from_user.id
            chat_id = message.chat.id
            member = await client.get_chat_member(chat_id, user_id)
            if member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
                return await func(client, message)
            else:
                return await message.reply("🚫 You need to be an admin to use this command.")
        except Exception as e:
            print(f"Admin check failed: {e}")
            return await message.reply("❌ Failed to check admin status.")
    return wrapper

async def mute(client, chat_id, user_id, duration=None):
    try:
        until_date = datetime.utcnow() + timedelta(seconds=duration) if duration else None
        permissions = ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_polls=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
            can_invite_users=False,
            can_pin_messages=False
        )
        await client.restrict_chat_member(chat_id, user_id, permissions=permissions, until_date=until_date)
        return True
    except Exception as e:
        print(f"Failed to mute user {user_id}: {e}")
        return False

async def unmute(client, chat_id, user_id):
    try:
        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_invite_users=True,
            can_pin_messages=True
        )
        await client.restrict_chat_member(chat_id, user_id, permissions=permissions)
        return True
    except Exception as e:
        print(f"Failed to unmute user {user_id}: {e}")
        return False

