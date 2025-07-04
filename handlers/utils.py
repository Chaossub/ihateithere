import json
import asyncio
from pyrogram.types import ChatPermissions
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserNotParticipant

# Path to warnings file (make sure this directory exists)
WARN_FILE = "data/warnings.json"

# ========== Admin-only Decorator ==========
def admin_only(func):
    async def wrapper(client, message):
        try:
            user_id = message.from_user.id
            chat_id = message.chat.id
            member = await client.get_chat_member(chat_id, user_id)
            if member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
                return await func(client, message)
            else:
                return await message.reply("🚫 You need to be an admin to use this command.")
        except UserNotParticipant:
            return await message.reply("🚫 You’re not a participant in this chat.")
        except Exception as e:
            print(f"admin_only error: {e}")
            return await message.reply("⚠️ Error checking admin status.")
    return wrapper

# ========== Mute & Unmute ==========
async def mute(client, chat_id, user_id, duration=None):
    try:
        permissions = ChatPermissions()  # Empty = mute all
        await client.restrict_chat_member(chat_id, user_id, permissions)
        if duration:
            # Unmute in the background after the duration (does not block bot)
            asyncio.create_task(unmute_later(client, chat_id, user_id, duration))
        return True
    except Exception as e:
        print(f"❌ Mute error: {e}")
        return False

async def unmute_later(client, chat_id, user_id, duration):
    await asyncio.sleep(duration)
    await unmute(client, chat_id, user_id)

async def unmute(client, chat_id, user_id):
    try:
        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_invite_users=True
        )
        await client.restrict_chat_member(chat_id, user_id, permissions)
        return True
    except Exception as e:
        print(f"❌ Unmute error: {e}")
        return False

# ========== Warning System ==========
def load_warns():
    try:
        with open(WARN_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_warns():
    try:
        with open(WARN_FILE, "w") as f:
            json.dump(_warns, f)
    except Exception as e:
        print(f"❌ save_warns error: {e}")

# These operate on a global dictionary _warns
_warns = load_warns()

def get_warns(chat_id, user_id):
    return _warns.get(str(chat_id), {}).get(str(user_id), 0)

def add_warn(chat_id, user_id, warns):
    chat_id = str(chat_id)
    user_id = str(user_id)
    if chat_id not in _warns:
        _warns[chat_id] = {}
    _warns[chat_id][user_id] = warns

def reset_warns(chat_id, user_id):
    chat_id = str(chat_id)
    user_id = str(user_id)
    if chat_id in _warns and user_id in _warns[chat_id]:
        _warns[chat_id][user_id] = 0

