import logging
import os

from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    CommandHandler, CallbackQueryHandler, PicklePersistence,  # CallbackQueryHandler,
)

from telebot.bot_src.client.publish_request import request_conv_handler
from telebot.bot_src.client.start import cmd_start_client
from telebot.bot_src.executor.start import cmd_start, submit_request
from telebot.bot_src.shared import CallBacks as cbg
from telebot.bot_src.executor.signup import conv_handeler
from telebot.bot_src.executor.executor_vars import (
    CallBacks as cb,
)

# from demo_menu import demo_menu

load_dotenv()
TOKEN_EXEC = os.getenv('TELEGRAM_TOKEN_EXECUTOR')
TOKEN_CLIENT = os.getenv('TELEGRAM_TOKEN_CLIENT')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# async def buttons(update: Update, context: CallbackContext):
#     keyboard = [[
#         InlineKeyboardButton(
#             text='Sign UP!!!',
#             callback_data=cbg.signup,
#         ),
#         InlineKeyboardButton(
#             text='Menu',
#             callback_data='hhh',
#         ),
#     ]]
#     # print('outside')
#     # query = update.callback_query
#     # await query.answer()
#     # if query.data == 'signup':
#     #     print('here')
#     #     return FIRST_NAME
#     query = update.callback_query
#     await query.answer()
#     await query.edit_message_reply_markup(InlineKeyboardMarkup(keyboard))


#     text = '''Please choose categories of requests you are working with:
# #social
# #children
# #work
# #loss
# #eatingbehaviour
# #partner
# #parents
# #trauma
# #obsessive
# #compulsive
# #personalcrisis
# #addiction'''
#     await msg_send(update, context, text)

# if __name__ == '__main__':
pikle_persist_executor = PicklePersistence('pikle_store_executor')
pikle_persist_client = PicklePersistence('pikle_store_client')
app_executor = ApplicationBuilder().token(TOKEN_EXEC).persistence(pikle_persist_executor).build()
app_client = ApplicationBuilder().token(TOKEN_CLIENT).persistence(pikle_persist_client).build()

app_executor.add_handler(CommandHandler('start', cmd_start))
app_executor.add_handler(conv_handeler)
app_executor.add_handler(CallbackQueryHandler(submit_request, '^request'))
# app_executor.add_handler(demo_menu)
# app_executor.add_handler(CommandHandler('signup', cmd_sign_up))
# app_executor.add_handler(CallbackQueryHandler(buttons, 'hhh'))

app_client.add_handler(CommandHandler('start', cmd_start_client))
app_client.add_handler(request_conv_handler)
# app_executor.run_polling()
