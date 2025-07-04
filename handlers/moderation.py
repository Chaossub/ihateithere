import json
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from handlers.utils import admin_only, mute, unmute, get_warns, add_warn, reset_warns, save_warns

WARN_FILE = "data/warnings.json"

@Client.on_message(filters.command("warn") & filters.group)
@admin_only
async def warn_user(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("⚠️ Reply to a user to warn them.")

    user_id = str(message.reply_to_message.from_user.id)
    chat_id = str(message.chat.id)
    warns = get_warns(chat_id, user_id) + 1
    add_warn(chat_id, user_id, warns)
    save_warns()

    if warns == 3:
        await mute(client, message.chat.id, message.reply_to_message.from_user.id, duration=300)
        await message.reply(f"🔇 User muted for 5 minutes after 3 warnings.")
    elif warns == 6:
        await mute(client, message.chat.id, message.reply_to_message.from_user.id, duration=600)
        await message.reply(f"🔇 User muted for 10 minutes after 6 warnings.")
    else:
        await message.reply(f"⚠️ User warned. Total warnings: {warns}")

@Client.on_message(filters.command("resetwarns") & filters.group)
@admin_only
async def reset_user_warns(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("⚠️ Reply to a user to reset their warnings.")

    user_id = str(message.reply_to_message.from_user.id)
    chat_id = str(message.chat.id)
    reset_warns(chat_id, user_id)
    save_warns()
    await message.reply("✅ Warnings reset.")

@Client.on_message(filters.command("warns") & filters.group)
@admin_only
async def check_warns(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("⚠️ Reply to a user to check their warnings.")

    user_id = str(message.reply_to_message.from_user.id)
    chat_id = str(message.chat.id)
    warns = get_warns(chat_id, user_id)
    await message.reply(f"⚠️ User has {warns} warnings.")

@Client.on_message(filters.command("mute") & filters.group)
@admin_only
async def mute_user(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("⚠️ Reply to a user to mute them.")

    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    try:
        if await mute(client, chat_id, user_id):
            await message.reply("🔇 User muted.")
        else:
            await message.reply("⚠️ Failed to mute.")
    except Exception as e:
        await message.reply(f"⚠️ Error: {e}")

@Client.on_message(filters.command("unmute") & filters.group)
@admin_only
async def unmute_user(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("⚠️ Reply to a user to unmute them.")

    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    try:
        if await unmute(client, chat_id, user_id):
            await message.reply("🔊 User unmuted.")
        else:
            await message.reply("⚠️ Failed to unmute.")
    except Exception as e:
        await message.reply(f"⚠️ Error: {

