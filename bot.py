from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a BIN (first 6–8 digits of a card) to check.")

async def check_bin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bin_number = update.message.text.strip()
    if not bin_number.isdigit() or not (6 <= len(bin_number) <= 8):
        await update.message.reply_text("Please enter a valid BIN (6–8 digits).")
        return

    response = requests.get(f"https://lookup.binlist.net/{bin_number}")
    if response.status_code != 200:
        await update.message.reply_text("Invalid BIN or service unavailable.")
        return

    data = response.json()
    reply = (
        f"💳 BIN: {bin_number}\n"
        f"Brand: {data.get('scheme', 'N/A').title()}\n"
        f"Type: {data.get('type', 'N/A').title()}\n"
        f"Bank: {data.get('bank', {}).get('name', 'N/A')}\n"
        f"Country: {data.get('country', {}).get('name', 'N/A')} ({data.get('country', {}).get('emoji', '')})"
    )
    await update.message.reply_text(reply)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_bin))

app.run_polling()
