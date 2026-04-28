import os
import telebot
from openai import OpenAI

# Отримуємо токени зі змінних середовища Railway
BOT_TOKEN = os.environ.get('BOT_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Я на зв'язку. Що цікавить?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Відправляємо запит до ChatGPT
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Можеш змінити на gpt-4o, якщо апік дозволяє
            messages=[
                {"role": "system", "content": "Ти розумний і лаконічний асистент."},
                {"role": "user", "content": message.text}
            ]
        )
        
        answer = response.choices[0].message.content
        bot.reply_to(message, answer)
        
    except Exception as e:
        print(f"Помилка: {e}")
        bot.reply_to(message, "Тут якась халепа з мізками (OpenAI). Перевір баланс або ключ.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
