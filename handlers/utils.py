from functools import wraps
from pyrogram.types import Message, ChatPermissions

# Path to warnings JSON
WARNINGS_FILE = "data/warnings.json"

# Ensure the warnings file exists
if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(WARNINGS_FILE):
    with open(WARNINGS_FILE, "w") as f:
        json.dump({}, f)

# Admin-only decorator
def admin_only(func):
    @wraps(func)
    async def wrapper(client, message: Message):
        user = message.from_user
        member = await client.get_chat_member(message.chat.id, user.id)
        if member.status not in ("administrator", "creator"):
            await message.reply("You need to be an admin to use this command.")
            return
        return await func(client, message)
    return wrapper

# Mute user
async def mute(app, chat_id, user_id, duration=None):
    permissions = ChatPermissions()
    try:
        await app.restrict_chat_member(chat_id, user_id, permissions, duration)
    except Exception as e:
        raise RuntimeError(f"Failed to mute: {e}")

# Unmute user
async def unmute(app, chat_id, user_id):
    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_invite_users=True
    )
    try:
        await app.restrict_chat_member(chat_id, user_id, permissions)
    except Exception as e:
        raise RuntimeError(f"Failed to unmute: {e}")

# Load warnings
def load_warns():
    with open(WARNINGS_FILE, "r") as f:
        return json.load(f)

# Save warnings
def save_warns(data):
    with open(WARNINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Get warns
def get_warns(user_id, chat_id):
    data = load_warns()
    return data.get(str(chat_id), {}).get(str(user_id), 0)

# Add warn
def add_warn(user_id, chat_id):
    data = load_warns()
    chat_id = str(chat_id)
    user_id = str(user_id)
    if chat_id not in data:
        data[chat_id] = {}
    data[chat_id][user_id] = data[chat_id].get(user_id, 0) + 1
    save_warns(data)

# Reset warns
def reset_warns(user_id, chat_id):
    data = load_warns()
    chat_id = str(chat_id)
    user_id = str(user_id)
    if chat_id in data and user_id in data[chat_id]:
        del data[chat_id][user_id]
        if not data[chat_id]:
            del data[chat_id]
    save_warns(data)
