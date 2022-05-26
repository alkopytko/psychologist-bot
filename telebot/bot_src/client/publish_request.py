from telegram import Update
from telegram.ext import CallbackContext

from .client_vars import (
    TextMessages as msg,
    Keyboards as kbd,
    UD as ud,
)
from .start import db_client
from ...models import Client, ClientRequest

PROBLEM, BUDGET = range(2)


async def enter_publish_request(update: Update, context: CallbackContext):
    await update.effective_chat.send_message(text=msg.request_enter)
    return PROBLEM


async def problem(update: Update, context: CallbackContext):
    context.user_data[ud.problem] = update.effective_message.text


async def budget(update: Update, context: CallbackContext):
    summ = update.effective_message.text
    if summ.isdigit():
        context.user_data[ud.budget] = int(summ)
        save_request_to_db(client=db_client(client=update.effective_user),
                           userdata=context.user_data)


def save_request_to_db(client: Client, userdata: dict):
    ClientRequest.objects.create(client=client,
                                 problem=userdata[ud.problem],
                                 budget=userdata[ud.budget]
                                 )
