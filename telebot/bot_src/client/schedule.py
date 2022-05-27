from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ConversationHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters, \
    CommandHandler

from telebot.bot_src.client.client_vars import (
    CallBacks as cb,
    UD as ud,
    TextMessages as msg,
    Keyboards as kbd,
)
from telebot.bot_src.client.db_queries_client import save_session_to_db
from telebot.bot_src.client.publish_request import cmd_cancel

ENTER_DATE = 0


async def schedule(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    _, executor_id, request_id = query.data.split(':')
    print(executor_id)
    context.user_data[ud.current_request] = request_id
    context.user_data[ud.current_request_executor] = executor_id
    await update.effective_chat.send_message(text=msg.enter_date)
    return ENTER_DATE


async def enter_date(update: Update, context: CallbackContext):
    context.user_data[ud.current_request_datetime] = update.effective_message.text
    call = sync_to_async(save_session_to_db)
    await call(context.user_data)
    await update.effective_chat.send_message(text=msg.schedule_success, reply_markup=kbd.start())
    return ConversationHandler.END


schedule_conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(schedule, '^' + cb.schedule)],
    states={
        ENTER_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_date)]
    },
    fallbacks=[CommandHandler('cancel', cmd_cancel)]
)
