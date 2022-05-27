from asgiref.sync import sync_to_async

from telebot.bot_src.client.db_queries_client import SessionExternal
from telebot.models import Executor, Client, Session


class ExecutorExternal:
    def __init__(self, user: Executor):
        self.user_id = user.user_id
        self.chat_id = user.chat_id
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.lang_level = user.lang_level
        self.photo = user.photo
        self.categories = [cat.category for cat in user.category.all()]
        self.scans = [scan.file for scan in user.certificate_set.all()]

    def __str__(self):
        return self.first_name


async def get_executor(user_id: int) -> ExecutorExternal:
    call = sync_to_async(extract_executor_from_db)
    return await call(user_id)


def extract_executor_from_db(user_id: int) -> ExecutorExternal:
    executor = Executor.objects.filter(user_id=user_id).first()
    return ExecutorExternal(executor) if executor else None


def get_sessions_executor(executor_id) -> list[SessionExternal]:
    out = []
    # client = Client.objects.filter(user_id=client_id).first()
    executor = Executor.objects.filter(user_id=executor_id).first()
    client_sessions = Session.objects.filter(executor=executor)
    for session in client_sessions:
        out.append(SessionExternal(session))
    return out