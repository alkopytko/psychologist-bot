from telegram import Update, User
from telegram.ext import CallbackContext
from .client_vars import (
    TextMessages as msg,
    Keyboards as kbd,
)
from ...models import Client


async def cmd_start_client(update: Update, context: CallbackContext):
    await update.effective_chat.send_message(text=msg.hello, reply_markup=kbd.start())


def db_client(client: User):
    client_obj, _ = Client.objects.get_or_create(user_id=client.id,
                                                 defaults={
                                                     'chat_id': client.id,
                                                     'name': client.first_name
                                                 })
    return client_obj
