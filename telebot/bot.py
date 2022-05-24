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

from .bot_src.shared import CallBacks as cbg
from .bot_src.signup import conv_handeler

# from demo_menu import demo_menu


load_dotenv()
TOKEN=os.getenv('TELEGRAM_TOKEN')


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def cmd_start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton(
            text='Sign UP',
            callback_data=cbg.signup,
        ),
        InlineKeyboardButton(
            text='Menu',
            callback_data='hhh',
        ),
    ]]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Hello Wold :)',
        reply_markup=markup
    )


async def buttons(update: Update, context: CallbackContext):
    keyboard = [[
        InlineKeyboardButton(
            text='Sign UP!!!',
            callback_data=cbg.signup,
        ),
        InlineKeyboardButton(
            text='Menu',
            callback_data='hhh',
        ),
    ]]
    # print('outside')
    # query = update.callback_query
    # await query.answer()
    # if query.data == 'signup':
    #     print('here')
    #     return FIRST_NAME
    query = update.callback_query
    await query.answer()
    await query.edit_message_reply_markup(InlineKeyboardMarkup(keyboard))


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
pikle_persist = PicklePersistence('pikle_store')
app = ApplicationBuilder().token(TOKEN).persistence(pikle_persist).build()

app.add_handler(CommandHandler('start', cmd_start))
app.add_handler(conv_handeler)
# app.add_handler(demo_menu)
# app.add_handler(CommandHandler('signup', cmd_sign_up))
app.add_handler(CallbackQueryHandler(buttons, 'hhh'))

# app.run_polling()
