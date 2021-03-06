import asyncio

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from telebot.bot_executor import app_executor
from ..bot_client import app_client

from .triggers_vars import (
    TextMessages as msg_trig
)

from telebot.bot_src.executor.executor_vars import (
    Keyboards as kbd,
    TextMessages as msg,
)
from ..models import ClientRequest, Executor, Session


def create_markup_to_request(request: ClientRequest):
    # print(request.id)
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
    await app_executor.bot.send_message(chat_id=executor_chat_id, text=msg_trig.approved_signup)
    await app_executor.bot.send_message(chat_id=executor_chat_id,
                                        text=msg.wellcome_registered,
                                        reply_markup=kbd.calendar())


async def send_submit_request(client_chat_id, text, reply_markup=None):
    await app_client.bot.send_message(chat_id=client_chat_id,
                                      text=text)


async def external_msg_to_executor(chat_id, text, reply_markup=None):
    await app_executor.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
    
def send_scheduled_session(session:Session):
    text = f'A new session scheduled with {session.client.name}\n' \
           f'You will get a link to session in 20 minutes before start'
    asyncio.run(external_msg_to_executor(session.executor.chat_id,text))