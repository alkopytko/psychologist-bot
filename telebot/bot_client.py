import logging
import os

from dotenv import load_dotenv
from telegram.ext import PicklePersistence, ApplicationBuilder, CommandHandler, CallbackQueryHandler

from telebot.bot_src.client.publish_request import request_conv_handler
from telebot.bot_src.client.schedule import schedule_conv_handler
from telebot.bot_src.client.start import calendar, cmd_start_client

from telebot.bot_src.client.client_vars import (
    CallBacks as cb_cl,
)

load_dotenv()
TOKEN_CLIENT = os.getenv('TELEGRAM_TOKEN_CLIENT')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

pikle_persist_client = PicklePersistence('pikle_store_client')
app_client = ApplicationBuilder().token(TOKEN_CLIENT).persistence(pikle_persist_client).build()

app_client.add_handler(CommandHandler('start', cmd_start_client))
app_client.add_handler(request_conv_handler)
app_client.add_handler(schedule_conv_handler)
app_client.add_handler(CallbackQueryHandler(calendar, cb_cl.consultations))