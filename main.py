import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")
PORT = int(os.getenv("PORT", 5000))

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

# --- Telegram command handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 MeetContractBot is running on Railway!")

# --- Create Application and add handlers ---
application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))

# --- Flask route for webhook ---
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.run(application.process_update(update))
    return "OK"

# --- Set webhook before starting Flask ---
print("Setting webhook...")
bot.set_webhook(f"{APP_URL}/{BOT_TOKEN}")
print(f"Webhook set to: {APP_URL}/{BOT_TOKEN}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
