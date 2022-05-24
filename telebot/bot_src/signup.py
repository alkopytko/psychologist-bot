from telegram import (
    Update,
)
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

from .shared import (
    msg_send,
    CallBacks as cbg,
)
from .signup_vars import (
    Keyboards as kbd,
    TextMessages as msg,
    CallBacks as cb,
    Categories as cat,
)

FIRST_NAME, LAST_NAME, SCANS, PHOTO, CATEGORIES, LANG_LEVEL, Q_CORRECT = range(7)


async def cmd_sign_up(update: Update, context: CallbackContext):
    context.user_data['categories'] = []
    await msg_send(update, context, msg.hello)
    await msg_send(update, context, msg.first_name)
    return FIRST_NAME


async def first_name(update: Update, context: CallbackContext):
    context.user_data['first_name'] = update.message.text
    await msg_send(update, context, msg.last_name)
    return LAST_NAME


async def last_name(update: Update, context: CallbackContext):
    context.user_data['last_name'] = update.message.text
    await msg_send(update, context, msg.scans, reply_markup=kbd.skip())
    return SCANS


async def skip_scans(update: Update, context: CallbackContext):
    await msg_send(update, context, msg.photo, reply_markup=kbd.skip())
    return PHOTO


async def scans(update: Update, context: CallbackContext):
    if update.message.document or update.message.photo:
        print('ok')
    else:
        print('not ok')
        text = 'please, upload a documents'
        await msg_send(update, context, text)
        return
    await msg_send(update, context, msg.photo, reply_markup=kbd.skip())
    return PHOTO


async def skip_photo(update: Update, context: CallbackContext):
    await msg_send(update, context, msg.categories, reply_markup=kbd.categories())
    return CATEGORIES


async def photo(update: Update, context: CallbackContext):
    if update.message.photo:
        print('ok')
    else:
        print('not ok')
        text = 'please, upload a photo'
        await msg_send(update, context, text)
        return
    await msg_send(update, context, msg.categories, reply_markup=kbd.categories())
    return CATEGORIES


async def categories(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    if query.data in context.user_data['categories']:
        context.user_data['categories'].remove(query.data)
        await query.edit_message_reply_markup(kbd.categories(context.user_data['categories']))
        return
    if query.data in cat.categories:
        context.user_data['categories'].append(query.data)
        await query.edit_message_reply_markup(kbd.categories(context.user_data['categories']))
        return
    if query.data == cb.done:
        await msg_send(update, context, msg.lang_level)
        return LANG_LEVEL


async def lang_level(update: Update, context: CallbackContext):
    await msg_send(update, context, msg.congratulations)
    return ConversationHandler.END


async def cmd_cancel(update: Update, context: CallbackContext):
    text = 'ok. cancel'
    await msg_send(update, context, text)
    return ConversationHandler.END


async def wrong(update: Update, context: CallbackContext):
    text = 'wrong data'
    await msg_send(update, context, text)


conv_handeler = ConversationHandler(
    entry_points=[
        CommandHandler('signup', cmd_sign_up),
        CallbackQueryHandler(cmd_sign_up, '^' + cbg.signup + '$'),
    ],
    states={
        FIRST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_name)],
        LAST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, last_name)],
        SCANS: [
            MessageHandler(~filters.COMMAND, scans),
            CallbackQueryHandler(skip_scans)
        ],
        PHOTO: [
            MessageHandler(~filters.COMMAND, photo),
            CallbackQueryHandler(skip_photo)
        ],
        CATEGORIES: [CallbackQueryHandler(categories)],
        LANG_LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, lang_level)],
    },
    fallbacks=[
        CommandHandler('cancel', cmd_cancel),
        MessageHandler(filters.ALL, wrong)
    ],
)
