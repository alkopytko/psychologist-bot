from telebot.bots import app_executor

from .triggers_vars import (
    TextMessages as msg
)



async def executor_approved(executor_chat_id:int):
    await app_executor.bot.send_message(chat_id=executor_chat_id,text=msg.approved_signup)
