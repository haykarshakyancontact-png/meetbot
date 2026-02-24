import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Bot Token & App URL ---
TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # Railway deployment URL, e.g., https://your-bot.up.railway.app
PORT = int(os.environ.get("PORT", "8443"))

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set")
if not APP_URL:
    raise ValueError("APP_URL environment variable not set")

# --- Telegram Bot Application ---
app_bot = ApplicationBuilder().token(TOKEN).build()

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 MeetContractBot is running on Railway!")

app_bot.add_handler(CommandHandler("start", start))

# --- Flask Web Server for Webhook ---
flask_app = Flask(__name__)

@flask_app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, app_bot.bot)
    app_bot.process_update(update)
    return "OK"

# --- Set Webhook and Run Flask ---
async def set_webhook():
    # Remove existing webhook (prevents conflicts)
    await app_bot.bot.delete_webhook()
    # Set new webhook
    await app_bot.bot.set_webhook(f"{APP_URL}/webhook/{TOKEN}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(set_webhook())
    # Run Flask app to receive updates
    flask_app.run(host="0.0.0.0", port=PORT)
