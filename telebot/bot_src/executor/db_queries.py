from asgiref.sync import sync_to_async

from telebot.models import Executor


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
