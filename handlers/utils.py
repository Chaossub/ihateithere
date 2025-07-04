import json
import asyncio
from pyrogram.types import ChatPermissions
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserNotParticipant

# ====== Admin-only Decorator ======
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

# ====== Mute / Unmute Functions ======
async def mute(client, chat_id, user_id, duration=None):
    try:
        permissions = ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_polls=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
            can_invite_users=False
        )
        await client.restrict_chat_member(chat_id, user_id, permissions)
        print(f"✅ Muted {user_id} in {chat_id}")
        if duration:
            await asyncio.sleep(duration)
            await unmute(client, chat_id, user_id)
        return True
    except Exception as e:
        print(f"❌ Mute error: {e}")
        return False

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
        print(f"✅ Unmuted {user_id} in {chat_id}")
        return True
    except Exception as e:
        print(f"❌ Unmute error: {e}")
        return False

# ====== Warnings JSON System ======
WARN_FILE = "data/warnings.json"

def load_warns():
    try:
        with open(WARN_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_warns(data=None):
    if data is None:
        data = warnings
    with open(WARN_FILE, "w") as f:
        js
