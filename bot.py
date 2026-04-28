import os
import logging
from collections import defaultdict, deque

import telebot
from dotenv import load_dotenv
from openai import OpenAI


# Завантажує .env локально. На Railway змінні беруться з Environment Variables.
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL", "gpt-5.2")
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "Ти розумний, практичний і лаконічний AI-асистент. "
    "Відповідай мовою користувача. Якщо питання складне — пояснюй структуровано."
)

if not BOT_TOKEN:
    raise RuntimeError("Немає BOT_TOKEN. Додай його в Railway Variables або .env")

if not OPENAI_API_KEY:
    raise RuntimeError("Немає OPENAI_API_KEY. Додай його в Railway Variables або .env")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)
client = OpenAI(api_key=OPENAI_API_KEY)

# Проста памʼять діалогу в RAM.
# Після перезапуску Railway історія очиститься — це нормально для першої версії.
chat_history = defaultdict(lambda: deque(maxlen=10))


def split_text(text: str, limit: int = 3900):
    """
    Telegram має ліміт приблизно 4096 символів на повідомлення.
    Ріжемо відповідь на частини з запасом.
    """
    if len(text) <= limit:
        return [text]

    parts = []
    while text:
        parts.append(text[:limit])
        text = text[limit:]
    return parts


def ask_openai(chat_id: int, user_text: str) -> str:
    """
    Відправляє повідомлення в OpenAI з короткою історією діалогу.
    """
    history = chat_history[chat_id]

    input_messages = []

    for item in history:
        input_messages.append(item)

    input_messages.append({
        "role": "user",
        "content": user_text
    })

    response = client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=input_messages
    )

    answer = response.output_text.strip()

    history.append({
        "role": "user",
        "content": user_text
    })

    history.append({
        "role": "assistant",
        "content": answer
    })

    return answer


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "Я на звʼязку. Напиши питання — відповім як AI-асистент."
    )


@bot.message_handler(commands=["help"])
def help_command(message):
    text = (
        "Команди:\n"
        "/start — запустити бота\n"
        "/help — допомога\n"
        "/reset — очистити памʼять цього чату\n\n"
        "Просто напиши повідомлення, і я відповім."
    )
    bot.reply_to(message, text)


@bot.message_handler(commands=["reset"])
def reset(message):
    chat_id = message.chat.id
    chat_history[chat_id].clear()
    bot.reply_to(message, "Памʼять цього чату очищена.")


@bot.message_handler(content_types=["text"])
def handle_text(message):
    chat_id = message.chat.id
    user_text = message.text.strip()

    if not user_text:
        bot.reply_to(message, "Напиши текстове повідомлення.")
        return

    try:
        bot.send_chat_action(chat_id, "typing")

        answer = ask_openai(chat_id, user_text)

        for part in split_text(answer):
            bot.send_message(chat_id, part)

    except Exception as e:
        logging.exception("Помилка під час обробки повідомлення")

        error_text = str(e).lower()

        if "rate limit" in error_text or "429" in error_text:
            bot.reply_to(message, "Забагато запитів. Спробуй ще раз трохи пізніше.")
        elif "authentication" in error_text or "api key" in error_text or "401" in error_text:
            bot.reply_to(message, "Проблема з OpenAI API key. Перевір ключ у Railway Variables.")
        elif "insufficient_quota" in error_text or "quota" in error_text or "billing" in error_text:
            bot.reply_to(message, "Проблема з балансом або лімітом OpenAI API.")
        else:
            bot.reply_to(message, "Сталася помилка. Перевір логи Railway.")


@bot.message_handler(content_types=[
    "photo", "video", "audio", "voice", "document", "sticker"
])
def handle_other(message):
    bot.reply_to(
        message,
        "Поки що я працюю тільки з текстом. Спочатку запускаємо стабільну текстову версію."
    )


if __name__ == "__main__":
    logging.info("Bot started with polling...")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
