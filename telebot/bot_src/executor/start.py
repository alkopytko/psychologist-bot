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


async def cmd_start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    executor = await get_executor(update.effective_user.id)
    if executor:
        await update.effective_user.send_message(text=msg.wellcome_registered,reply_markup=kbd.calendar())
        return
    else:
        await update.effective_user.send_message(text=msg.wellcome_unregistered, reply_markup=kbd.signup())

