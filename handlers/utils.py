from pyrogram.types import ChatPermissions
from pyrogram.errors import RPCError
from config import SUPERUSERS
import json
import os
from datetime import timedelta

# --- Admin Check Decorator ---
def admin_only(func):
    async def wrapper(client, message):
        user_id = message.from_user.id
        if user_id in SUPERUSERS:
            return await func(client, message)
        chat_member = await client.get_chat_member(message.chat.id, user_id)
        if chat_member.status in ["administrator", "creator"]:
            return await func(client, message)
        return await message.reply("You don't have permission to use this command.")
    return wrapper

# --- Mute / Unmute Functions ---
async def mute(client, chat_id, user_id, duration_seconds=None):
    try:
        until_date = None
        if duration_seconds:
            until_date = int((timedelta(seconds=duration_seconds)).total_seconds()) + int(client.get_me().id)

        permissions = ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_stickers=False,
            can_send_animations=False,
            can_send_games=False,
            can_use_inline_bots=False,
            can_add_web_page_previews=False,
            can_send_polls=False,
            can_invite_users=False,
            can_change_info=False,
            can_pin_messages=False
        )
        await client.restrict_chat_member(chat_id, user_id, permissions, until_date=until_date)
        return True
    except RPCError as e:
        print(f"Failed to mute: {e}")
        return False

async def unmute(client, chat_id, user_id):
    try:
        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_stickers=True,
            can_send_animations=True,
            can_send_games=True,
            can_use_inline_bots=True,
            can_add_web_page_previews=True,
            can_send_polls=True,
            can_invite_users=True,
            can_change_info=False,
            can_pin_messages=False
        )
        await client.restrict_chat_member(chat_id, user_id, permissions)
        return True
    except RPCError as e:
        print(f"Failed to unmute: {e}")
        return False

# --- Warning System Functions ---
def get_warns():
    if not os.path.exists("warns.json"):
        return {}
    with open("warns.json", "r") as f:
        return json.load(f)

def save_warns(warns):
    with open("warns.json", "w") as f:
        json.dump(warns, f, indent=2)

def add_warn(user_id):
    warns = get_warns()
    user_id = str(user_id)
    if user_id not in warns:
        warns[user_id] = 0
    warns[user_id] += 1
    save_warns(warns)
    return warns[user_id]

def reset_warns(user_id):
    warns = get_warns()
    user_id = str(user_id)
    warns[user_id] = 0
    save_warns(warns)
