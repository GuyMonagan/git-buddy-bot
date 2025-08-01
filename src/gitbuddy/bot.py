from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from gitbuddy.config import TOKEN
from gitbuddy.menu import MENU_STRUCTURE


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
        "Выбери команду Git:"
        if update.callback_query
        else "Привет! Я GitBuddyBot.\n"
        "Помогаю вспомнить команды Git.\n"
        "Выбери, с чем тебе нужна помощь 👇"
    )

    if update.callback_query:
        query = update.callback_query
        if query.message.text != message or query.message.reply_markup != reply_markup:
            await query.edit_message_text(text=message, reply_markup=reply_markup)

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
            menu_stack[user_id].append(key)
            context.user_data["expecting_commit"] = True
            context.user_data["command_prefix"] = item.get(
                "command_prefix", 'git commit -m "'
            )
            context.user_data["command_suffix"] = item.get("command_suffix", '"')
            prompt = item.get("input_prompt", "Введи сообщение:")
            await query.edit_message_text(prompt)

        elif item.get("handler"):
            handler_func = globals().get(item["handler"])
            if handler_func:
                await handler_func(update, context)
            else:
                await query.edit_message_text("🤖 Ошибка: не удалось найти обработчик.")

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
    В режиме custom_input — собирает сообщение и генерирует команду.
    """

    if context.user_data.get("expecting_commit"):
        text = update.message.text
        command_prefix = context.user_data.get("command_prefix", 'git commit -m "')
        command_suffix = context.user_data.get("command_suffix", '"')
        command = f"{command_prefix}{text}{command_suffix}"
        message = f"Готово! Вот твоя команда:\n\n```bash\n{command}\n```"
        context.user_data["expecting_commit"] = False
        context.user_data.pop("command_prefix", None)
        context.user_data.pop("command_suffix", None)

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


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = """
\u26a0\ufe0f *ВАЖНО*

1. Команды, скопированные из Telegram, могут сразу исполняться в терминале. Будь осторожен.
   Лучше сначала вставь в текстовый редактор.

2. Git отслеживает файлы, даже если ты добавил их в `.gitignore`,
   если они уже были закоммичены ранее.

3. Бот всё ещё развивается. Если что-то сломалось — нажми /start или покричи в подушку.

4. Никакой магии. Только кнопки, Markdown и Python.

Сделано с болью, потом и *ChatGPT Monday*.
"""
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔙 Назад", callback_data="__back")]]
    )
    await update.callback_query.edit_message_text(
        message, parse_mode="Markdown", reply_markup=reply_markup
    )


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("🤖 Бот запущен. Нажмите Ctrl+C, чтобы остановить.")
    app.run_polling()
