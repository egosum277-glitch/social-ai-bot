def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, normal_message))

    print("Бот запущений...")
    app.run_polling()


if __name__ == "__main__":
    main()
