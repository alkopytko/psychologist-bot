from telegram import Update
from .client_vars import (
    TextMessages as msg,
    Keyboards as kbd,
)

from telegram.ext import CallbackContext


async def cmd_start_client(update: Update, context: CallbackContext):
    await update.effective_chat.send_message(text=msg.hello, reply_markup=kbd.start())


async def calendar(update: Update, context: CallbackContext):
    pass