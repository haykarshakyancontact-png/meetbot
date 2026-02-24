import os
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# ==============================
# Environment
# ==============================
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables")

PORT = int(os.environ.get("PORT", 10000))

# ==============================
# Telegram Command Handlers
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to MeetContractBot!\n\n"
        "Use /new_meetup to create a meetup.\n"
        "Use /help to see commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Available Commands:\n"
        "/start - Start the bot\n"
        "/new_meetup - Create a meetup\n"
        "/help - Show this help message"
    )

async def new_meetup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎉 Meetup creation coming soon!"
    )

# ==============================
# Flask App (Render Requires This)
# ==============================

app = Flask(__name__)

@app.route("/")
def home():
    return "MeetContractBot is running!"

# ==============================
# Telegram App Setup
# ==============================

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("new_meetup", new_meetup))

# ==============================
# Main
# ==============================

async def main():
    # Start Telegram bot
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    app.run(host="0.0.0.0", port=PORT)
