from pyrogram import filters
from pyrogram.types import Message
from models.db import feds_col
from handlers.utils import admin_only
import random

def random_id():
    return str(random.randint(10000, 99999))

def register(app):

    # ✅ Federation test creation
    @app.on_message(filters.command("createfedtest") & filters.group)
    async def test_createfed(client, message: Message):
        test_data = {
            "fed_id": "99999",
            "name": "Test Federation",
            "owner_id": message.from_user.id,
            "admins": [message.from_user.id],
            "groups": [message.chat.id],
            "banned_users": [],
        }
        try:
            feds_col.insert_one(test_data)
            await message.reply("✅ Test federation created.")
        except Exception as e:
            await message.reply(f"❌ Failed to create federation:\n<code>{e}</code>")

    # ✅ Create federation
    @app.on_message(filters.command("createfed") & filters.group)
    @admin_only
    async def create_fed_handler(client, message: Message):
        fed_name = " ".join(message.command[1:]) or "My Federation"
        chat_id = message.chat.id
        owner_id = message.from_user.id
        fed_id = random_id()
        existing = feds_col.find_one({"groups": chat_id})
        if existing:
            await message.reply("❌ This group is already in a federation.")
            return
        fed_doc = {
            "fed_id": fed_id,
            "name": fed_name,
            "owner_id": owner_id,
            "admins": [owner_id],
            "groups": [chat_id],
            "banned_users": [],
        }
        feds_col.insert_one(fed_doc)
        await message.reply(f"✅ Federation created!\nID: <code>{fed_id}</code>\nName: <b>{fed_name}</b>")

    # ✅ Link group
    @app.on_message(filters.command("linkfed") & filters.group)
    @admin_only
    async def linkfed_handler(client, message: Message):
        args = message.text.split()
        if len(args) < 2:
            await message.reply("Usage: /linkfed <fed_id>")
            return
        fed_id = args[1]
        chat_id = message.chat.id
        fed = feds_col.find_one({"fed_id": fed_id})
        if not fed:
            await message.reply("❌ Federation not found.")
            return
        if chat_id in fed.get("groups", []):
            await message.reply("❌ This group is already linked.")
            return
        feds_col.update_one({"fed_id": fed_id}, {"$addToSet": {"groups": chat_id}})
        await message.reply("✅ Group linked to federation.")

    # ✅ Add admin
    @app.on_message(filters.command("addfedadmin") & filters.group)
    @admin_only
    async def addfedadmin_handler(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user to make them a federation admin.")
            return
        user = message.reply_to_message.from_user
        fed = feds_col.find_one({"groups": message.chat.id})
        if not fed or fed["owner_id"] != message.from_user.id:
            await message.reply("❌ Only the federation owner can add admins.")
            return
        feds_col.update_one({"fed_id": fed["fed_id"]}, {"$addToSet": {"admins": user.id}})
        await message.reply(f"✅ {user.mention} added as federation admin.")

    # ✅ Remove admin
    @app.on_message(filters.command("delfedadmin") & filters.group)
    @admin_only
    async def delfedadmin_handler(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user to remove them as federation admin.")
            return
        user = message.reply_to_message.from_user
        fed = feds_col.find_one({"groups": message.chat.id})
        if not fed or fed["owner_id"] != message.from_user.id:
            await message.reply("❌ Only the federation owner can remove admins.")
            return
        feds_col.update_one({"fed_id": fed["fed_id"]}, {"$pull": {"admins": user.id}})
        await message.reply(f"✅ {user.mention} removed as federation admin.")

    # ✅ FedBan
    @app.on_message(filters.command("fedban") & filters.group)
    @admin_only
    async def fedban_handler(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user to federation ban them.")
            return
        user = message.reply_to_message.from_user
        fed = feds_col.find_one({"groups": message.chat.id})
        if not fed or message.from_user.id not in fed.get("admins", []):
            await message.reply("❌ Only federation admins can fedban.")
            return
        if user.id in fed.get("banned_users", []):
            await message.reply("User is already federationally banned.")
            return
        feds_col.update_one({"fed_id": fed["fed_id"]}, {"$addToSet": {"banned_users": user.id}})
        await message.reply(f"🚫 {user.mention} is now federationally banned.")

    # ✅ FedUnban
    @app.on_message(filters.command("fedunban") & filters.group)
    @admin_only
    async def fedunban_handler(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user to federation unban them.")
            return
        user = message.reply_to_message.from_user
        fed = feds_col.find_one({"groups": message.chat.id})
        if not fed or message.from_user.id not in fed.get("admins", []):
            await message.reply("❌ Only federation admins can fedunban.")
            return
        feds_col.update_one({"fed_id": fed["fed_id"]}, {"$pull": {"banned_users": user.id}})
        await message.reply(f"✅ {user.mention} has been federation unbanned.")

    # ✅ FedCheck
    @app.on_message(filters.command("fedcheck") & filters.group)
    async def fedcheck_handler(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user to check their federation ban status.")
            return
        user = message.reply_to_message.from_user
        fed = feds_col.find_one({"groups": message.chat.id})
        if not fed:
            await message.reply("❌ This group is not part of any federation.")
            return
        if user.id in fed.get("banned_users", []):
            await message.reply(f"🚫 {user.mention} is federationally banned.")
        else:
            await message.reply(f"✅ {user.mention} is NOT federationally banned.")

    # ✅ Rename federation
    @app.on_message(filters.command("renamefed") & filters.group)
    @admin_only
    async def renamefed_handler(client, message: Message):
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.reply("Usage: /renamefed <new_name>")
            return
        new_name = args[1]
        fed = feds_col.find_one({"groups": message.chat.id})
        if not fed or fed["owner_id"] != message.from_user.id:
            await message.reply("❌ Only the federation owner can rename the fed.")
            return
        feds_col.update_one({"fed_id": fed["fed_id"]}, {"$set": {"name": new_name}})
        await message.reply(f"✅ Federation renamed to <b>{new_name}</b>.")

    # ✅ Delete federation
    @app.on_message(filters.command("delfed") & filters.group)
    @admin_only
    async def delfed_handler(client, message: Message):
        fed = feds_col.find_one({"groups": message.chat.id})
        if not fed or fed["owner_id"] != message.from_user.id:
            await message.reply("❌ Only the federation owner can delete the fed.")
            return
        feds_col.delete_one({"fed_id": fed["fed_id"]})
        await message.reply("❌ Federation deleted.")


