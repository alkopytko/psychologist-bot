from pathlib import Path

from asgiref.sync import sync_to_async
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

from telebot.bot_src.shared import (
    msg_send,
    CallBacks as cbg,
    UPLOAD_PATH,
)
from .executor_vars import (
    Keyboards as kbd,
    TextMessages as msg,
    CallBacks as cb,
    Categories as cat,
    UD as ud
)
from telebot.models import Executor, Category, Certificate

FIRST_NAME, LAST_NAME, SCANS, PHOTO, CATEGORIES, LANG_LEVEL, Q_CORRECT = range(7)


async def cmd_sign_up(update: Update, context: CallbackContext):
    context.user_data[ud.categories] = []
    # context.user_data[ud.path] = UPLOAD_PATH.joinpath(str(update.effective_user.id))
    context.user_data[ud.media_group] = None
    context.user_data[ud.scan_list] = []
    await msg_send(update, context, msg.signup_hello)
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
    file=None
    if update.message.document:
        file = await update.effective_message.effective_attachment.get_file()
    if update.message.photo:
        file = await update.effective_message.effective_attachment[-1].get_file()
    if file:
        # file = update.effective_message.effective_attachment.file_name
        # file = await update.effective_message.effective_attachment.file_name
        # with open(file.file_id, 'wb') as f:
        #     downloaded_scan = await file.download(out=f)
        # downloaded_scan = await file.download(custom_path=context.user_data['path'])
        # downloaded_scan = await file.download(custom_path=UPLOAD_PATH)
        file_ext=Path(update.effective_message.effective_attachment.file_name).suffix
        downloaded_scan = await file.download(custom_path=UPLOAD_PATH.joinpath(file.file_id+file_ext))
        context.user_data[ud.scan_list].append(downloaded_scan)
        if (
                context.user_data[ud.media_group] != update.effective_message.media_group_id
                or context.user_data[ud.media_group] is None
        ):
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
        # downloaded_photo = await file.download(custom_path=context.user_data[ud.path])
        downloaded_photo = await file.download(custom_path=UPLOAD_PATH.joinpath(file.file_id+'.jpg'))
        context.user_data[ud.photo] = downloaded_photo
        await msg_send(update, context, msg.categories, reply_markup=kbd.categories())
        return CATEGORIES
    else:
        text = 'Please, upload a jpg photo or set compress checkbox'
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
    async_save_to_db = sync_to_async(save_to_db, thread_sensitive=False)

    await async_save_to_db(update, context)

    return ConversationHandler.END


def save_to_db(update: Update, context: CallbackContext):
    cats=Category.objects.filter(category__in=context.user_data[ud.categories])
    executor, _ = Executor.objects.get_or_create(
        user_id=update.effective_user.id,
        defaults={
            'chat_id': update.effective_chat.id,
            'first_name': context.user_data[ud.first_name],
            'last_name': context.user_data[ud.last_name],
            'photo': context.user_data[ud.photo].name,
            'lang_level': context.user_data[ud.lang_level]
        },
    )
    executor.category.add(*cats)
    executor.save()
    for scan in context.user_data[ud.scan_list]:
        Certificate.objects.create(file=scan.name,executor=executor)

    # str_first_name = str(context.user_data[ud.first_name]) + '\n'
    # str_last_name = str(context.user_data[ud.last_name]) + '\n'
    # str_scans = ' ,'.join([str(i) for i in context.user_data[ud.scan_list]]) + '\n'
    # str_photo = str(context.user_data[ud.photo]) + '\n'
    # str_categories = ' ,'.join(context.user_data[ud.categories]) + '\n'
    # str_lang_level = str(context.user_data[ud.lang_level]) + '\n'
    #
    # text = str_first_name + str_last_name + str_scans + str_categories + str_lang_level
    # await msg_send(update, context, text)
    # await update.effective_user.send_photo(open(context.user_data[ud.photo], 'rb'))


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
        CallbackQueryHandler(cmd_sign_up, '^' + cb.signup + '$'),
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
