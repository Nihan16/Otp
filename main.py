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

# ➕ /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running!\nSend your 2FA secret code to get the OTP.")

# 🔐 Convert 2FA Secret to OTP
async def get_otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    secret = update.message.text.strip().replace(" ", "")
    try:
        totp = pyotp.TOTP(secret)
        otp = totp.now()
        await update.message.reply_text(f"🔐 OTP: `{otp}`", parse_mode="Markdown")
    except:
        await update.message.reply_text("❌ Invalid 2FA secret. Try again.")

# ✅ Start the bot (no asyncio.run!)
def main():
    keep_alive()  # run Flask web server
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_otp))
    print("Bot is running...")
    app.run_polling()  # direct call, no asyncio.run()

# 🔁 Launch
if __name__ == '__main__':
    main()
