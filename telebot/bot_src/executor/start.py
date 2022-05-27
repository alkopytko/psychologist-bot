from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from telebot.bot_src.executor.db_queries import get_executor
from telebot.bot_src.shared import CallBacks as cbg

from .executor_vars import (
    Keyboards as kbd,
    TextMessages as msg,
    CallBacks as cb,
    Categories as cat,
    UD as ud
)
# from ..triggers import send_submit_request


async def cmd_start(update: Update, context: CallbackContext):
    executor = await get_executor(update.effective_user.id)
    if executor:
        await update.effective_user.send_message(text=msg.wellcome_registered, reply_markup=kbd.calendar())
        return
    else:
        await update.effective_user.send_message(text=msg.wellcome_unregistered, reply_markup=kbd.signup())


async def submit_request(update: Update, context: CallbackContext):
    from ...bots import app_client

    query = update.callback_query
    await query.answer()
    _, client_chat_id, request_id = query.data.split(':')
    text = f'hohoho {client_chat_id} {request_id}'
    # await send_submit_request(client_chat_id=client_chat_id,
    #                           text=text)
    await app_client.bot.send_message(chat_id=client_chat_id, text=text)
