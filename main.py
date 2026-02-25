import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")
PORT = int(os.getenv("PORT", "5000"))

bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)

# Dispatcher handles incoming updates
dispatcher = Dispatcher(bot, None, workers=0)

# Command handler
def start(update: Update, context):
    update.message.reply_text("👋 MeetContractBot is running on Railway!")

dispatcher.add_handler(CommandHandler("start", start))

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

# Set webhook when app starts
@app.before_first_request
def set_webhook():
    bot.set_webhook(f"{APP_URL}/{BOT_TOKEN}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
