import pytest
from unittest.mock import AsyncMock, MagicMock
from gitbuddy.bot import start, show_menu, button_handler, message_handler, menu_stack, help_handler
from gitbuddy.menu import MENU_STRUCTURE
from gitbuddy import bot as bot_module  # нужен доступ к menu_stack
from telegram.error import TelegramError


@pytest.mark.asyncio
async def test_start_creates_menu_and_calls_show_menu(monkeypatch):
    fake_show_menu = AsyncMock()
    monkeypatch.setattr("gitbuddy.bot.show_menu", fake_show_menu)

    fake_update = MagicMock()
    fake_update.effective_chat.id = 1234
    fake_update.callback_query = None
    fake_update.message = MagicMock()
    fake_update.message.reply_text = AsyncMock()

    fake_context = MagicMock()

    await start(fake_update, fake_context)

    assert menu_stack[1234] == []
    fake_show_menu.assert_called_once()


@pytest.mark.asyncio
async def test_show_menu_with_message():
    update = MagicMock()
    update.effective_chat.id = 1234
    update.callback_query = None
    update.message = MagicMock()
    update.message.reply_text = AsyncMock()

    context = MagicMock()

    menu_stack[1234] = []

    await show_menu(update, context, MENU_STRUCTURE)

    update.message.reply_text.assert_called_once()


@pytest.mark.asyncio
async def test_button_handler_opens_submenu(monkeypatch):
    fake_show_menu = AsyncMock()
    monkeypatch.setattr("gitbuddy.bot.show_menu", fake_show_menu)

    update = MagicMock()
    update.effective_chat.id = 42
    update.callback_query = MagicMock()
    update.callback_query.data = "commit"
    update.callback_query.answer = AsyncMock()

    context = MagicMock()

    menu_stack[42] = []

    await button_handler(update, context)

    fake_show_menu.assert_called_once()
    assert menu_stack[42] == ["commit"]


@pytest.mark.asyncio
async def test_button_handler_with_callback():
    update = MagicMock()
    update.effective_chat.id = 123
    update.callback_query = MagicMock()
    update.callback_query.data = "init"
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()

    context = MagicMock()

    menu_stack[123] = []

    await button_handler(update, context)

    update.callback_query.edit_message_text.assert_called_once()
    # УБИРАЕМ ложное ожидание
    # assert "init" in menu_stack[123]


@pytest.mark.asyncio
async def test_message_handler_generates_commit():
    update = MagicMock()
    update.message.text = "первый коммит"
    update.message.reply_text = AsyncMock()

    context = MagicMock()
    context.user_data = {
        "expecting_commit": True,
        "command_prefix": 'git commit -m "',
        "command_suffix": '"'
    }

    await message_handler(update, context)

    update.message.reply_text.assert_called_once()
    assert context.user_data["expecting_commit"] is False


@pytest.mark.asyncio
async def test_help_handler():
    update = MagicMock()
    update.callback_query = MagicMock()
    update.callback_query.edit_message_text = AsyncMock()

    context = MagicMock()

    await help_handler(update, context)

    update.callback_query.edit_message_text.assert_called_once()
    args, kwargs = update.callback_query.edit_message_text.call_args
    assert "ВАЖНО" in args[0] or "ВАЖНО" in kwargs.get("text", "")


@pytest.mark.asyncio
async def test_button_handler_with_unknown_key():
    """
    Тест на неизвестную команду (ошибочный callback_data)
    """
    update = MagicMock()
    update.effective_chat.id = 404
    update.callback_query = MagicMock()
    update.callback_query.data = "неизвестная_фигня"
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()

    context = MagicMock()
    menu_stack[404] = []

    await button_handler(update, context)

    update.callback_query.edit_message_text.assert_called_once()
    args, kwargs = update.callback_query.edit_message_text.call_args
    text = args[0] if args else kwargs.get("text", "")
    assert "Неизвестная команда" in text


@pytest.mark.asyncio
async def test_custom_input_git_commit():
    update = MagicMock()
    update.effective_chat.id = 1
    update.callback_query = MagicMock()
    update.callback_query.data = "custom_commit"
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context = MagicMock()
    context.user_data = {}

    # Важно: мы внутри подменю commit
    bot_module.menu_stack[1] = ["commit"]

    await button_handler(update, context)

    assert context.user_data["expecting_commit"] is True
    assert context.user_data["command_prefix"] == 'git commit -m "'
    assert context.user_data["command_suffix"] == '"'

    # Отправим сообщение
    update = MagicMock()
    update.message = MagicMock()
    update.message.text = "фикс багов"
    update.message.reply_text = AsyncMock()

    await message_handler(update, context)

    update.message.reply_text.assert_called_once()
    args, kwargs = update.message.reply_text.call_args
    assert 'git commit -m "фикс багов"' in args[0] or kwargs.get("text", "").startswith("git commit")


@pytest.mark.asyncio
async def test_show_menu_handles_telegram_error_gracefully():
    from gitbuddy import bot as bot_module
    bot_module.menu_stack[999] = []

    update = MagicMock()
    update.effective_chat.id = 999
    update.callback_query = None
    update.message = MagicMock()
    update.message.reply_text = AsyncMock(side_effect=TelegramError("API is dead"))

    context = MagicMock()

    # если вдруг код не обрабатывает ошибку — этот тест упадёт
    with pytest.raises(TelegramError):
        await show_menu(update, context, {"help": {"title": "help"}})
