from telegram import User

from telebot.bot_src.client.client_vars import UD as ud
from telebot.models import Client, ClientRequest, Session, Executor


def db_client(client: User):
    client_obj, _ = Client.objects.get_or_create(user_id=client.id,
                                                 defaults={
                                                     'chat_id': client.id,
                                                     'name': client.first_name
                                                 })
    return client_obj


def save_request_to_db(client: Client, userdata: dict):
    obj = ClientRequest.objects.create(client=client,
                                       problem=userdata[ud.problem],
                                       budget=userdata[ud.budget]
                                       )
    return obj.id


def get_request(request_id):
    obj = ClientRequest.objects.filter(id=request_id).first()
    return obj or None


def get_executor(executor_id):
    return Executor.objects.filter(user_id=executor_id).first()


def get_client(client_id):
    return Client.objects.filter(user_id=client_id).first()


def save_session_to_db(userdata: dict):
    request = get_request(userdata[ud.current_request])
    executor=get_executor(userdata[ud.current_request_executor])
    print(executor)
    obj = Session.objects.create(
        client=request.client,
        executor=get_executor(userdata[ud.current_request_executor]),
        request=request,
        date_time=userdata[ud.current_request_datetime]
    )
    return obj.id
