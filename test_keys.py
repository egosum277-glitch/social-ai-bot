import os
import urllib.request
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL", "gpt-5.2")


def test_env():
    assert BOT_TOKEN, "BOT_TOKEN відсутній"
    assert OPENAI_API_KEY, "OPENAI_API_KEY відсутній"
    print("ENV OK")


def test_telegram():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"

    with urllib.request.urlopen(url, timeout=15) as response:
        data = json.loads(response.read().decode("utf-8"))

    assert data.get("ok") is True, f"Telegram token bad: {data}"
    print("Telegram OK:", data["result"]["username"])


def test_openai():
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.responses.create(
        model=MODEL,
        input="Відповідай тільки одним словом: OK"
    )

    print("OpenAI OK:", response.output_text)


if __name__ == "__main__":
    test_env()
    test_telegram()
    test_openai()
