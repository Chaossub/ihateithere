import os
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "SuccuBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode=ParseMode.HTML
)

@app.on_message(filters.command("ping"))
async def ping_handler(client, message):
    print("Received /ping!")
    await message.reply("pong!")

print("✅ SuccuBot is running...")
app.run()
