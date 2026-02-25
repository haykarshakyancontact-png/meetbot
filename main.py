import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler

TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # Railway URL
PORT = int(os.environ.get("PORT", 5000))

if not TOKEN or not APP_URL:
    raise ValueError("BOT_TOKEN or APP_URL environment variable not set")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, update_queue=None, workers=0)

app = Flask(__name__)

# Example /start command
def start(update: Update, context):
    update.message.reply_text("👋 MeetContractBot is running on Railway!")

dp.add_handler(CommandHandler("start", start))

# Webhook route for Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dp.process_update(update)
    return "OK"

# Health check route
@app.route("/")
def index():
    return "Bot is alive!"

if __name__ == "__main__":
    # Set webhook automatically on start
    bot.set_webhook(f"{APP_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=PORT)
