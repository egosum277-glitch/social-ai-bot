import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Я бот-генерал 🧠\n\n"
        "Команди:\n"
        "/status — перевірити систему\n"
        "/help — список команд\n"
        "/ai текст — AI-завдання"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Команди:\n"
        "/status — статус системи\n"
        "/ai Напиши опис для відео про каву"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Система активна ✅\n"
        "Генерал працює 🧠\n"
        "Telegram-модуль: готовий ✅\n"
        "AI-модуль: ще не підключений ⏳"
    )

async def ai_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)

    if not text:
        await update.message.reply_text("Напиши так:\n/ai Напиши опис для відео")
        return

    await update.message.reply_text(
        "AI-завдання прийнято 🧠\n\n"
        f"Задача: {text}\n\n"
        "AI-мозок підключимо наступним кроком."
    )

async def normal_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Ти написав: {update.message.text}"
    )

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("ai", ai_task))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, normal_message))

    print("Бот-генерал запущений...")
    app.run_polling()

if __name__ == "__main__":
    main()
