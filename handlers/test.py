from pyrogram import filters
from pyrogram.types import Message
from models.db import feds_col

def register(app):
    @app.on_message(filters.command("dbtest") & filters.group)
    async def dbtest_handler(client, message: Message):
        try:
            count = feds_col.count_documents({})
            await message.reply(f"✅ MongoDB is connected. Federation count: {count}")
        except Exception as e:
            await message.reply(f"❌ MongoDB error:\n<code>{e}</code>")
