from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

from config import TOKEN

COMMANDS = {
    "init": {
        "title": "Создание репозитория",
        "explanation": "`git init` — создаёт новый пустой Git-репозиторий в текущей папке.",
        "command": "git init"
    },
    "add": {
        "title": "Добавление файлов",
        "explanation": "`git add .` — добавляет все изменения в рабочей директории к следующему коммиту.",
        "command": "git add ."
    },
    "commit": {
        "title": "Коммит",
        "explanation": "`git commit -m \"сообщение\"` — сохраняет текущие изменения с комментарием.",
        "command": "git commit -m \"сообщение\""
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(COMMANDS[key]["title"], callback_data=key)]
        for key in COMMANDS
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Привет! Я GitBuddyBot. Нажми на команду, чтобы узнать о ней больше:",
        reply_markup=reply_markup
    )
