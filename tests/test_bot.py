import pytest
from unittest.mock import AsyncMock, MagicMock
from bot import start, menu_stack, show_menu, MENU_STRUCTURE


@pytest.mark.asyncio
async def test_start_creates_menu_and_calls_show_menu(monkeypatch):
    # Подготовка: мок-шоу_меню
    fake_show_menu = AsyncMock()
    monkeypatch.setattr("bot.show_menu", fake_show_menu)

    # Мок апдейта и контекста
    fake_update = MagicMock()
    fake_update.effective_chat.id = 1234
    fake_update.callback_query = None
    fake_update.message = MagicMock()

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

    # Предварительно закидываем юзера в стек
    from bot import menu_stack
    menu_stack[1234] = []

    await show_menu(update, context, MENU_STRUCTURE)

    update.message.reply_text.assert_called_once()


@pytest.mark.asyncio
async def test_button_handler_opens_submenu(monkeypatch):
    from bot import button_handler, menu_stack

    # Подменим show_menu
    fake_show_menu = AsyncMock()
    monkeypatch.setattr("bot.show_menu", fake_show_menu)

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
async def test_message_handler_generates_commit():
    from bot import message_handler

    update = MagicMock()
    update.message.text = "первый коммит"
    update.message.reply_text = AsyncMock()

    context = MagicMock()
    context.user_data = {"expecting_commit": True}

    await message_handler(update, context)

    update.message.reply_text.assert_called_once()
    assert context.user_data["expecting_commit"] is False


import pytest
from unittest.mock import AsyncMock, MagicMock
from bot import button_handler, menu_stack

@pytest.mark.asyncio
async def test_button_handler_with_callback(monkeypatch):
    # Мокаем update и context
    update = MagicMock()
    update.effective_chat.id = 123
    update.callback_query = MagicMock()
    update.callback_query.data = "init"
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()

    context = MagicMock()

    # Предварительный контекст
    menu_stack[123] = []

    await button_handler(update, context)

    update.callback_query.edit_message_text.assert_called_once()
    assert "init" in menu_stack[123]
