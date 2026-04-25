async def normal_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    msg = await update.message.reply_text("Думаю... 🧠")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ти корисний AI-асистент. Відповідай українською просто і коротко."},
                {"role": "user", "content": user_text}
            ],
            timeout=20
        )

        answer = response.choices[0].message.content
        await msg.edit_text(answer)

    except Exception as e:
        await msg.edit_text(f"Помилка AI ⚠️\n\n{str(e)}")
