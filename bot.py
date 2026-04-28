import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("8715926645:AAEG6r1KjH-QwXTxh3uJzSfuf8Lq4NYLc_0")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Я працюю 24/7 🚀")

async def normal_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Ти написав: {update.message.text}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, normal_message))

    print("Бот запущений...")
    app.run_polling()

if __name__ == "__main__":
    main()
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Система активна ✅\n"
        "Генерал працює 🧠\n"
        "Telegram-модуль готовий ✅\n"
        "AI-модуль підключений ✅"
    )
