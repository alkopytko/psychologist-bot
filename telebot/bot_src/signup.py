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
    UPLOAD_PATH,
)
from .signup_vars import (
    Keyboards as kbd,
    TextMessages as msg,
    CallBacks as cb,
    Categories as cat,
    UD as ud
)

FIRST_NAME, LAST_NAME, SCANS, PHOTO, CATEGORIES, LANG_LEVEL, Q_CORRECT = range(7)


async def cmd_sign_up(update: Update, context: CallbackContext):
    context.user_data[ud.categories] = []
    context.user_data[ud.path] = UPLOAD_PATH.joinpath(str(update.effective_user.id))
    context.user_data[ud.media_group] = None
    context.user_data[ud.scan_list] = []
    await msg_send(update, context, msg.hello)
    await msg_send(update, context, msg.first_name)
    return FIRST_NAME


async def first_name(update: Update, context: CallbackContext):
    context.user_data[ud.first_name] = update.message.text
    await msg_send(update, context, msg.last_name)
    return LAST_NAME


async def last_name(update: Update, context: CallbackContext):
    context.user_data[ud.last_name] = update.message.text
    await msg_send(update, context, msg.scans, reply_markup=kbd.skip())
    return SCANS


async def skip_scans(update: Update, context: CallbackContext):
    await msg_send(update, context, msg.photo, reply_markup=kbd.skip())
    return PHOTO


async def scans(update: Update, context: CallbackContext):
    if update.message.document or update.message.photo:
        file = await update.effective_message.effective_attachment.get_file()
        downloaded_scan = await file.download(custom_path=context.user_data['path'])
        context.user_data[ud.scan_list].append(downloaded_scan)
        if context.user_data[ud.media_group] != update.effective_message.media_group_id:
            await msg_send(update, context, msg.scans_wait_done, reply_markup=kbd.done())
            context.user_data[ud.media_group] = update.effective_message.media_group_id
    else:
        text = 'Please, upload a documents'
        await msg_send(update, context, text, kbd.skip())


async def skip_photo(update: Update, context: CallbackContext):
    await msg_send(update, context, msg.categories, reply_markup=kbd.categories())
    return CATEGORIES


async def photo(update: Update, context: CallbackContext):
    if update.message.photo:
        file = await update.effective_message.effective_attachment[-1].get_file()
        downloaded_photo = await file.download(custom_path=context.user_data[ud.path])
        context.user_data[ud.photo] = downloaded_photo
        await msg_send(update, context, msg.categories, reply_markup=kbd.categories())
        return CATEGORIES
    else:
        text = 'Please, upload a photo'
        await msg_send(update, context, text, kbd.skip())
        return


async def categories(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    if query.data in context.user_data[ud.categories]:
        context.user_data[ud.categories].remove(query.data)
        await query.edit_message_reply_markup(kbd.categories(context.user_data[ud.categories]))
        return
    if query.data in cat.categories:
        context.user_data[ud.categories].append(query.data)
        await query.edit_message_reply_markup(kbd.categories(context.user_data[ud.categories]))
        return
    if query.data == cb.done:
        await msg_send(update, context, msg.lang_level)
        return LANG_LEVEL


async def lang_level(update: Update, context: CallbackContext):
    context.user_data[ud.lang_level] = update.message.text
    await msg_send(update, context, msg.congratulations)
    await confirmation(update, context)
    return ConversationHandler.END


async def confirmation(update: Update, context: CallbackContext):
    first_name=context.user_data[ud.first_name]+'\n'
    last_name=context.user_data[ud.last_name]+'\n'
    scans=' ,'.join(context.user_data[ud.scan_list])+'\n'
    photo=context.user_data[ud.photo]+'\n'
    categories=' ,'.join(context.user_data[ud.categories])+'\n'
    lang_level=context.user_data[ud.lang_level]+'\n'

    text=first_name+last_name+scans+photo+categories+lang_level
    await msg_send(update, context, text)


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
        # MessageHandler(filters.ALL, wrong)
    ],
)
