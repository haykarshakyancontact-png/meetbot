import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

# Get bot token from environment
TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))  # your telegram user id

if not TOKEN:
    raise ValueError("BOT_TOKEN not found")

# In-memory storage for responses
meetups = {}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 MeetContractBot is running on Railway!")

# Start meetup
async def meetup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Agree ✅", callback_data="agree"),
            InlineKeyboardButton("Not Agree ❌", callback_data="not_agree"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = await update.message.reply_text(
        "Do you agree to meet up?", reply_markup=reply_markup
    )
    # Store responses keyed by message id
    meetups[msg.message_id] = {}

# Handle button presses
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    message_id = query.message.message_id

    # Record user's response
    meetups.setdefault(message_id, {})
    meetups[message_id][user.username] = query.data

    await query.answer(f"You selected: {query.data}")

    # Update message with current responses
    status = "\n".join([f"{u}: {r}" for u, r in meetups[message_id].items()])
    await query.message.edit_text(
        f"Current responses:\n{status}", reply_markup=query.message.reply_markup
    )

    # Notify owner if 3 people have responded
    if len(meetups[message_id]) >= 3 and OWNER_ID != 0:
        responses_summary = "\n".join(
            [f"{u}: {r}" for u, r in meetups[message_id].items()]
        )
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=f"📣 Meetup completed! Responses:\n{responses_summary}",
        )

# Build the bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("meetup", meetup))
app.add_handler(CallbackQueryHandler(button_handler))

# Run polling
if __name__ == "__main__":
    print("👋 MeetContractBot is running!")
    app.run_polling()
