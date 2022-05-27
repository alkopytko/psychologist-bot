from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import CallbackContext

from telebot.bot_src.executor.db_queries import get_executor, get_sessions_executor

from .executor_vars import (
    Keyboards as kbd,
    TextMessages as msg
)
from ..client.client_vars import Keyboards as kbd_cli
# from ..triggers import send_submit_request


async def cmd_start(update: Update, context: CallbackContext):
    executor = await get_executor(update.effective_user.id)
    if executor:
        if executor.approved:
            await update.effective_user.send_message(text=msg.wellcome_registered, reply_markup=kbd.calendar())
        else:
            await update.effective_user.send_message(text=msg.congratulations)
        return
    else:
        await update.effective_user.send_message(text=msg.wellcome_unregistered, reply_markup=kbd.signup())


async def submit_request(update: Update, context: CallbackContext):
    from ...bot_client import app_client

    query = update.callback_query
    await query.answer()
    _, client_chat_id, request_id = query.data.split(':')
    executor = await get_executor(update.effective_user.id)
    text = f'Your request submitted by {executor.first_name}\n' \
           f'...(Some additional info about {executor.first_name} plus button "See profile")'
    from telebot.bot_src.triggers import send_submit_request
    # await send_submit_request(client_chat_id=client_chat_id,
    #                           text=text)

    await app_client.bot.send_message(chat_id=client_chat_id,
                                      text=text,
                                      reply_markup=kbd_cli.schedule(executor.user_id,request_id))
    await update.effective_chat.send_message('Submitted')

async def calendar_executor(update: Update, context: CallbackContext):
    call = sync_to_async(get_sessions_executor)
    sessions = await call(update.effective_user.id)
    if sessions:
        for session in sessions:
            text=f'Session with {session.client.name}\n' \
                 f'Date: {session.date_time}'
            await update.effective_chat.send_message(text=text)
    else:
        await update.effective_chat.send_message('There are no sessions scheduled')
        await cmd_start(update, context)


