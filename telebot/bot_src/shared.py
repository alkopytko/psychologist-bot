from pathlib import Path

from telegram import Update
from telegram.ext import CallbackContext

PROJECT_PATH = Path.cwd()
UPLOAD_DIR = 'upload'
UPLOAD_PATH = PROJECT_PATH.joinpath(UPLOAD_DIR)


async def msg_send(update: Update, context: CallbackContext, text: str, reply_markup=None):
    return await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=reply_markup,
    )


# async def file_name(attachment:TelegramObject):
#     extension=attachment.file_name


# async def msg_edit(update: Update, context: CallbackContext, text: str, reply_markup=None):
#     if context.chat_data.get('emsg'):
#         msg: telegram.Message = context.chat_data['emsg']
#         await msg.edit_text(text=text, reply_markup=reply_markup)


class CallBacks:
    signup = 'signup'
