from keep_alive import keep_alive
import pyotp
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ✅ Replace with your bot token
BOT_TOKEN = "8189221727:AAG0XsAystYJJRw97MkR8wyZB7VYcsvkHJs"

# ➕ Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running!\nSend your 2FA secret code to get the OTP.")

# 🔑 Message handler: 2FA secret → OTP
async def get_otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    secret = update.message.text.strip().replace(" ", "")  # clean spaces
    try:
        totp = pyotp.TOTP(secret)
        otp = totp.now()
        await update.message.reply_text(f"🔐 OTP: `{otp}`", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text("❌ Invalid 2FA secret. Try again.")

# ✅ Main bot setup
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_otp))
    keep_alive()
    print("Bot is running...")
    await app.run_polling()

# 🔁 Run the bot
import asyncio
asyncio.run(main())
