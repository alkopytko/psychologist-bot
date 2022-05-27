import logging
import os
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    PicklePersistence,
)

from telebot.bot_src.executor.executor_vars import (
    CallBacks as cb_ex,
)
from telebot.bot_src.executor.signup import conv_handeler
from telebot.bot_src.executor.start import cmd_start, submit_request, calendar_executor

load_dotenv()
TOKEN_EXEC = os.getenv('TELEGRAM_TOKEN_EXECUTOR')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

pikle_persist_executor = PicklePersistence('pikle_store_executor')
app_executor = ApplicationBuilder().token(TOKEN_EXEC).persistence(pikle_persist_executor).build()

app_executor.add_handler(CommandHandler('start', cmd_start))
app_executor.add_handler(conv_handeler)
app_executor.add_handler(CallbackQueryHandler(submit_request, '^request'))
app_executor.add_handler(CallbackQueryHandler(calendar_executor, cb_ex.calendar))


async def external_msg_to_executor(chat_id, text, reply_markup=None):
    await app_executor.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
