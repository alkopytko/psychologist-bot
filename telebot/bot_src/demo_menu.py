# from telegram import (
#     Update,
#     InlineKeyboardButton,
#     InlineKeyboardMarkup,
# )
# from telegram.ext import (
#     CallbackContext,
#     ConversationHandler,
#     CommandHandler,
#     CallbackQueryHandler, MessageHandler, filters,
# )
#
# import callbacks as cb
#
# MENU = 0
#
# keyboard_enter = [
#     [
#         InlineKeyboardButton('Option1', callback_data='opt1'),
#         InlineKeyboardButton('Option2', callback_data='opt2'),
#     ],
# ]
# keyboard_o1 = [
#     [
#         InlineKeyboardButton('Option3', callback_data='opt3'),
#         InlineKeyboardButton('Option4', callback_data='opt4'),
#     ],
# ]
# keyboard_o2 = [
#     [
#         InlineKeyboardButton('Option5', callback_data='opt5'),
#         InlineKeyboardButton('Option6', callback_data='opt6'),
#     ],
# ]
#
#
# def kbd_with_back(back_opt, keyboard=None):
#     btn_text = 'Back'
#     cb_data = 'back' + str(back_opt)
#     if back_opt == 'home':
#         btn_text = 'Exit'
#         cb_data = 'exit'
#     if keyboard is None:
#         keyboard = []
#     return keyboard + [[InlineKeyboardButton(btn_text, callback_data=cb_data), ]]
#
#
# async def msg_send(update: Update, context: CallbackContext, text: str, reply_markup=None):
#     await context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text=text,
#         reply_markup=reply_markup,
#     )
#
#
# async def home(update: Update, context: CallbackContext):
#     keyboard = [[
#         InlineKeyboardButton(
#             text='Sign UP',
#             callback_data=cb.SIGNUP,
#         ),
#         InlineKeyboardButton(
#             text='Menu',
#             callback_data='hhh',
#         ),
#     ]]
#     text = 'thx :)'
#     markup = InlineKeyboardMarkup(keyboard)
#     await msg_send(update, context, text, markup)
#     return ConversationHandler.END
#
#
# async def wrong(update: Update, context: CallbackContext):
#     text = 'something wrong'
#     await msg_send(update, context, text)
#
#
# async def enter(update: Update, context: CallbackContext):
#     back = 'home'
#     text = 'Select an option:'
#     markup = InlineKeyboardMarkup(kbd_with_back(back, keyboard_enter))
#     await msg_send(update, context, text, markup)
#     return MENU
#
#
# async def option1(update: Update, context: CallbackContext):
#     back = 'enter'
#     text = 'Select another option:'
#     markup = InlineKeyboardMarkup(kbd_with_back(back, keyboard_o1))
#     await msg_send(update, context, text, markup)
#
#
# async def option2(update: Update, context: CallbackContext):
#     back = 'enter'
#     text = 'Select another option:'
#     markup = InlineKeyboardMarkup(kbd_with_back(back, keyboard_o2))
#     await msg_send(update, context, text, markup)
#
#
# async def option3(update: Update, context: CallbackContext):
#     back = 'opt1'
#     text = 'Text of options 3'
#     markup = InlineKeyboardMarkup(kbd_with_back(back, ))
#     await msg_send(update, context, text, markup)
#
#
# async def option4(update: Update, context: CallbackContext):
#     back = 'opt1'
#     text = 'Text of options 4'
#     markup = InlineKeyboardMarkup(kbd_with_back(back, ))
#     await msg_send(update, context, text, markup)
#
#
# async def option5(update: Update, context: CallbackContext):
#     back = 'opt2'
#     text = 'Text of options 5'
#     markup = InlineKeyboardMarkup(kbd_with_back(back, ))
#     await msg_send(update, context, text, markup)
#
#
# async def option6(update: Update, context: CallbackContext):
#     back = 'opt2'
#     text = 'Text of options 6'
#     markup = InlineKeyboardMarkup(kbd_with_back(back, ))
#     await msg_send(update, context, text, markup)
#
#
# async def menu(update: Update, context: CallbackContext):
#     menu_switch = {
#         'backenter': enter,
#         'backopt1': option1,
#         'backopt2': option2,
#         'opt1': option1,
#         'opt2': option2,
#         'opt3': option3,
#         'opt4': option4,
#         'opt5': option5,
#         'opt6': option6,
#     }
#     query = update.callback_query
#     await query.answer()
#     await menu_switch.get(query.data, wrong)(update, context)
#
#
# async def timeout(update: Update, context: CallbackContext):
#     text='timeout'
#     await msg_send(update, context, text)
#
#
# demo_menu = ConversationHandler(
#     entry_points=[CallbackQueryHandler(enter, 'hhh')],
#     states={
#         MENU: [
#             CallbackQueryHandler(home, 'exit'),
#             CallbackQueryHandler(menu)
#         ],
#         ConversationHandler.TIMEOUT: [
#             CallbackQueryHandler(timeout)
#         ]
#     },
#     fallbacks=[
#         CommandHandler('start', home),
#     ],
#     conversation_timeout=10.0
# )
