from asgiref.sync import sync_to_async
from telegram import Update
from .client_vars import (
    TextMessages as msg,
    Keyboards as kbd,
)

from telegram.ext import CallbackContext

from .db_queries_client import get_sessions_client


async def cmd_start_client(update: Update, context: CallbackContext):
    await update.effective_chat.send_message(text=msg.hello, reply_markup=kbd.start())


async def calendar(update: Update, context: CallbackContext):
    call = sync_to_async(get_sessions_client)
    sessions = await call(update.effective_user.id)
    if sessions:
        for session in sessions:
            text=f'Session with {session.executor.first_name}\n' \
                 f'Date: {session.date_time}'
            await update.effective_chat.send_message(text=text)
    else:
        await update.effective_chat.send_message('There are no sessions scheduled')
        await cmd_start_client(update, context)

