import os

try:
    from pyrogram import Client, filters
    from pyrogram.enums import ParseMode
    from dotenv import load_dotenv
except Exception as import_err:
    print("Failed to import libraries:", import_err)
    raise

print("Imports successful.")

# Load environment variables from .env if present
load_dotenv()
print("Loaded .env (if present).")

try:
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    assert API_ID and API_HASH and BOT_TOKEN, "API_ID, API_HASH, or BOT_TOKEN is missing!"

    API_ID = int(API_ID)
except Exception as config_err:
    print("Error with environment variables or config:", config_err)
    raise

print("Environment variables loaded.")

try:
    app = Client(
        "SuccuBot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        parse_mode=ParseMode.HTML
    )
    print("Pyrogram Client created.")
except Exception as client_err:
    print("Failed to initialize Pyrogram Client:", client_err)
    raise

# --- TEST HANDLER ---
@app.on_message(filters.command("ping"))
async def ping_handler(client, message):
    print("Received /ping!")
    await message.reply("pong")

try:
    from handlers import (
        welcome,
        help_cmd,
        moderation,
        federation,
        summon,
        xp,
        fun
    )
    print("Handlers imported successfully.")
except Exception as handler_err:
    print("Failed to import handlers:", handler_err)
    raise

print("==== [STARTING BOT LOOP] ====")

try:
    app.run()
except Exception as run_err:
    print("Bot failed to run:", run_err)
    raise

