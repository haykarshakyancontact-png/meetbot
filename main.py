import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Dispatcher

# Environment variables
TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # Your Railway URL, e.g., https://your-project.up.railway.app
PORT = int(os.getenv("PORT", 5000))  # Use Railway PORT or default to 5000

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set")
if not APP_URL:
    raise ValueError("APP_URL environment variable not set")

# Telegram bot setup
bot = Bot(TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 MeetContractBot is running on Railway!")

dispatcher.add_handler(CommandHandler("start", start))

# Webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# Set webhook with Telegram
@app.before_first_request
def setup_webhook():
    bot.delete_webhook()
    bot.set_webhook(url=f"{APP_URL}/{TOKEN}")

# Run Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
