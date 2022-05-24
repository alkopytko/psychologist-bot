from telegram import Update
from telegram.ext import CallbackContext


async def msg_send(update: Update, context: CallbackContext, text: str, reply_markup=None):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=reply_markup,
    )

class CallBacks:
    signup = 'signup'