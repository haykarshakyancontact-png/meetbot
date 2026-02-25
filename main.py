import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Environment variables
TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # Railway URL
PORT = int(os.environ.get("PORT", 5000))

if not TOKEN or not APP_URL:
    raise ValueError("BOT_TOKEN or APP_URL environment variable not set")

# Flask app
app = Flask(__name__)

# Telegram command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 MeetContractBot is running on Railway!")

# ApplicationBuilder (modern python-telegram-bot)
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

# Webhook route
@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "OK"

# Health check route
@app.route("/")
def index():
    return "Bot is alive!"

# Run the app
if __name__ == "__main__":
    # Set webhook automatically on start
    import asyncio
    asyncio.run(application.bot.set_webhook(f"{APP_URL}/{TOKEN}"))
    app.run(host="0.0.0.0", port=PORT)
