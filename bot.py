from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,   # вот он
    ContextTypes,
    filters            # и он
)


from config import TOKEN

COMMANDS = {
    "init": {
        "title": "Создание репозитория",
        "explanation": "`git init` — создаёт новый пустой Git-репозиторий в текущей папке.",
        "command": "git init",
    },
    "add": {
        "title": "Добавление файлов",
        "explanation": "`git add .` — добавляет все изменения в рабочей директории к следующему коммиту.",
        "command": "git add .",
    },
    "commit": {
        "title": "Коммит",
        "explanation": '`git commit -m "сообщение"` — сохраняет текущие изменения с комментарием.',
        "command": 'git commit -m "сообщение"',
    },
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Отправляет стартовое сообщение с кнопками выбора Git-команд.

    Пользователь получает приветствие и клавиатуру с доступными Git-командами.
    """
    keyboard = [
        [InlineKeyboardButton(COMMANDS[key]["title"], callback_data=key)]
        for key in COMMANDS
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Привет! Я GitBuddyBot. Нажми на команду, чтобы узнать о ней больше:",
        reply_markup=reply_markup,
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает нажатие кнопок в интерфейсе Telegram.

    В зависимости от callback_data:
    - Показывает информацию о выбранной Git-команде
    - Или возвращает меню, если нажата кнопка 'Назад'
    """
    query = update.callback_query
    await query.answer()

    key = query.data

    if key in COMMANDS:
        data = COMMANDS[key]
        message = f"🔹 *{data['title']}*\n\n{data['explanation']}\n\n```\n{data['command']}\n```"
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Назад", callback_data="back")]
        ])
        await query.edit_message_text(text=message, parse_mode="Markdown", reply_markup=reply_markup)

    elif key == "back":
        keyboard = [
            [InlineKeyboardButton(COMMANDS[k]["title"], callback_data=k)]
            for k in COMMANDS
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="Выбери команду Git:",
            reply_markup=reply_markup
        )

    else:
        await query.edit_message_text(text="Неизвестная команда 🤷‍♂️")


async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает текстовые сообщения, которые не являются командами.

    Если пользователь пишет в чат вручную, бот отвечает, что он понимает только кнопки.
    """
    await update.message.reply_text(
        "Извини, я понимаю только команды через кнопки. Нажми /start, если запутался."
    )


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_message))


    print("🤖 Бот запущен. Нажмите Ctrl+C, чтобы остановить.")
    app.run_polling()



