from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CallbackQueryHandler, MessageHandler, filters, \
    CommandHandler

from .client_vars import (
    TextMessages as msg,
    Keyboards as kbd,
    UD as ud,
    CallBacks as cb,
)
from .db_queries_client import db_client, save_request_to_db

PROBLEM, BUDGET = range(2)


async def enter_publish_request(update: Update, context: CallbackContext):
    await update.effective_chat.send_message(text=msg.ask_problem)
    return PROBLEM


async def problem(update: Update, context: CallbackContext):
    context.user_data[ud.problem] = update.effective_message.text
    await update.effective_chat.send_message(text=msg.ask_budget)
    return BUDGET


async def problem_wrong(update: Update, context: CallbackContext):
    await update.effective_chat.send_message(text=msg.wrong_problem_data)


async def budget(update: Update, context: CallbackContext):
    summ = update.effective_message.text
    if summ.isdigit():
        context.user_data[ud.budget] = int(summ)
        async_save_request_to_db = sync_to_async(save_request_to_db, thread_sensitive=False)
        async_db_client = sync_to_async(db_client, thread_sensitive=False)
        request_id = await async_save_request_to_db(client=await async_db_client(client=update.effective_user),
                                                    userdata=context.user_data)
        additional_text = f'\nYour request id: {request_id}'
        await update.effective_chat.send_message(text=msg.request_success + additional_text)
        return ConversationHandler.END
    else:
        await update.effective_chat.send_message(text=msg.wrong_budget_data)


async def budget_wrong(update: Update, context: CallbackContext):
    await update.effective_chat.send_message(text=msg.wrong_problem_data)


async def cmd_cancel(update: Update, context: CallbackContext):
    await update.effective_chat.send_message(text=msg.cancel, reply_markup=kbd.start())
    return ConversationHandler.END


request_conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(enter_publish_request, cb.request)],
    states={
        PROBLEM: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, problem),
            MessageHandler(~filters.COMMAND, problem_wrong)
        ],
        BUDGET: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, budget),
            MessageHandler(~filters.COMMAND, budget_wrong)
        ],
    },
    fallbacks=[CommandHandler('cancel', cmd_cancel)]
)
