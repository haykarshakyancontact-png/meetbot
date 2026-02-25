import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")
PORT = int(os.getenv("PORT", 5000))

if not TOKEN:
    raise ValueError("BOT_TOKEN not set")
if not APP_URL:
    raise ValueError("APP_URL not set")

application = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 MeetContractBot is running on Railway!")

application.add_handler(CommandHandler("start", start))

flask_app = Flask(__name__)

@flask_app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"

@flask_app.route("/")
def home():
    return "Bot is alive"

async def setup():
    await application.initialize()
    await application.bot.delete_webhook()
    await application.bot.set_webhook(f"{APP_URL}/{TOKEN}")

if __name__ == "__main__":
    asyncio.run(setup())
    flask_app.run(host="0.0.0.0", port=PORT)
