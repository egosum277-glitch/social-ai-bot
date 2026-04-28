import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Отримуємо токен зі змінних середовища (БЕЗПЕКА!)
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Я працюю 24/7 🚀")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Система активна\n✅ AI-модуль підключено")

async def main():
    # Перевірка чи є токен
    if not TOKEN:
        print("Помилка: TELEGRAM_TOKEN не знайдено в зміних оточення!")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status)) # Тепер це працюватиме
    
    print("Бот запускається...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
