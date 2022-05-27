import asyncio

from asgiref.sync import async_to_sync
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext


from .triggers_vars import (
    TextMessages as msg
)
from ..models import ClientRequest, Executor

from telebot.bots import app_executor


def create_markup_to_request(request: ClientRequest):
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton('Submit', callback_data=f'request:{request.client.chat_id}:{request.id}')]])


def send_request_to_all_executors(request: ClientRequest):
    text = f'Request from {request.client.name}:\n' \
           f'{request.problem}\n' \
           f'Budges is {request.budget}$ per session'
    executors = Executor.objects.values_list('chat_id', flat=True)
    asyncio.run(send_message_to_list_of_chat_id(
        chat_id_list=[*executors],
        text=text,
        reply_markup=create_markup_to_request(request)))
    # call = async_to_sync(send_message_to_list_of_chat_id)
    # call(chat_id_list=[*executors], text=text)


async def send_message_to_list_of_chat_id(chat_id_list, text, reply_markup=None):

    for chat_id in chat_id_list:
        await app_executor.bot.send_message(chat_id=chat_id,
                                            text=text,
                                            reply_markup=reply_markup)


async def executor_approved(executor_chat_id: int):
    await app_executor.bot.send_message(chat_id=executor_chat_id, text=msg.approved_signup)


async def submit_request(update: Update, context: CallbackContext):
    from telebot.bots import app_client
    query = update.callback_query
    await query.answer()
    _, client_chat_id, request_id = query.data.split(':')
    text = 'hohoho'
    await app_client.bot.send_message(chat_id=client_chat_id,
                                      text=text)
