from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import TOKEN
from menu import MENU_STRUCTURE

menu_stack = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает команду /start. Показывает приветствие и вызывает главное меню.
    """
    menu_stack[update.effective_chat.id] = []
    await show_menu(update, context, MENU_STRUCTURE)


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, menu):
    """
    Показывает главное меню с кнопками команд.
    Может быть вызвано при старте или при нажатии 'Назад'.
    """
    keyboard = [
        [InlineKeyboardButton(menu[key]["title"], callback_data=key)] for key in menu
    ]
    if menu_stack[update.effective_chat.id]:
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="__back")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    message = (
        "Выбери команду Git:" if update.callback_query else "Привет! Я GitBuddyBot."
    )

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=message, reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(text=message, reply_markup=reply_markup)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает нажатие кнопок в интерфейсе Telegram.

    В зависимости от callback_data:
    поддержка навигации по меню
    """
    user_id = update.effective_chat.id

    if user_id not in menu_stack:
        menu_stack[user_id] = []

    query = update.callback_query
    await query.answer()

    key = query.data
    current_menu = MENU_STRUCTURE
    for step in menu_stack.get(user_id, []):
        current_menu = current_menu[step].get("submenu", {})

    if key == "__back":
        if menu_stack[user_id]:
            menu_stack[user_id].pop()

        # 🔧 восстановим текущее меню после шага назад
        current_menu = MENU_STRUCTURE
        for step in menu_stack[user_id]:
            current_menu = current_menu[step].get("submenu", {})

        await show_menu(update, context, current_menu)
        return

    if key in current_menu:
        item = current_menu[key]
        if "submenu" in item:
            menu_stack[user_id].append(key)
            await show_menu(update, context, item["submenu"])
        elif item.get("custom_input"):
            menu_stack[user_id].append(key)  # 🧠 Запоминаем путь
            context.user_data["expecting_commit"] = True
            await query.edit_message_text("Введи сообщение для коммита:")

        else:
            menu_stack[user_id].append(key)  # <== ВОТ ЭТО — твой пропуск обратно

            message = f"🔹 *{item['title']}*\n\n{item['explanation']}\n\n```\n{item['command']}\n```"
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Назад", callback_data="__back")]]
            )
            await query.edit_message_text(
                text=message, parse_mode="Markdown", reply_markup=reply_markup
            )

    else:
        await query.edit_message_text(text="Неизвестная команда 🤷‍♂️")


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает текстовые сообщения, не являющиеся командами.
    В режиме custom_commit — собирает сообщение и генерирует команду.
    """

    if context.user_data.get("expecting_commit"):
        text = update.message.text
        command = f'git commit -m "{text}"'
        message = f"Готово! Вот твоя команда:\n\n```bash\n{command}\n```"
        context.user_data["expecting_commit"] = False

        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Назад", callback_data="__back")]]
        )

        await update.message.reply_text(
            message, parse_mode="Markdown", reply_markup=reply_markup
        )

    else:
        await update.message.reply_text(
            "Извини, я понимаю только команды через кнопки. Нажми /start, если запутался."
        )


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("🤖 Бот запущен. Нажмите Ctrl+C, чтобы остановить.")
    app.run_polling()
