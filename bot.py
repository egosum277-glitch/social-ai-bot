import os
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Я AI-генерал 🧠\n\n"
        "Пиши мені будь-яке питання — я відповім як ChatGPT.\n\n"
        "Команди:\n"
        "/status — перевірити систему\n"
        "/help — допомога"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Команди:\n\n"
        "/status — статус системи\n"
        "/help — допомога\n\n"
        "Або просто напиши повідомлення — і я відповім як AI."
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Система активна ✅\n"
        "Генерал працює 🧠\n"
        "Telegram-модуль: готовий ✅\n"
        "AI-модуль: підключений ✅"
    )

async def normal_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    await update.message.reply_text("Думаю... 🧠")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Ти AI-генерал. Відповідай українською мовою. "
                    "Пиши просто, зрозуміло, як для новачка. "
                    "Будь корисним, конкретним і не вигадуй фактів."
                )
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    )

    ai_answer = response.choices[0].message.content
    await update.message.reply_text(ai_answer)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, normal_message))

    print("AI-генерал запущений...")
    app.run_polling()

if __name__ == "__main__":
    main()
