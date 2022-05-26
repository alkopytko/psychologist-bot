import asyncio

from django.core.management.base import BaseCommand
from telegram import InputMediaDocument

from telebot.bots import app
from telebot.bot_src.shared import UPLOAD_PATH
from telebot.models import Executor


class Profile:
    def __init__(self, user: Executor):
        self.chat_id = user.chat_id
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.lang_level = user.lang_level
        self.photo = user.photo
        self.categories = [cat.category for cat in user.category.all()]
        self.scans = [scan.file for scan in user.certificate_set.all()]


async def profile_text(chat_id, text):
    await app.bot.send_message(chat_id=chat_id, text=text)


async def photosend(chat_id, filename):
    await app.bot.send_photo(chat_id=chat_id, photo=open(UPLOAD_PATH.joinpath(filename), 'rb'))


async def groupfilesend(chat_id, filename_list):
    media = [InputMediaDocument(open(UPLOAD_PATH.joinpath(i), 'rb')) for i in filename_list]
    await app.bot.send_media_group(chat_id=chat_id, media=media)


async def async_handle(profiles_list):
    for profile in profiles_list:
        text = 'First name: ' + profile.first_name + '\n' + \
               'Last name: ' + profile.last_name + '\n' + \
               'Language level: ' + profile.lang_level + '\n' + \
        'Categories: ' + ', '.join(profile.categories) + '\n'

    await photosend(chat_id=profile.chat_id, filename=profile.photo)
    await profile_text(chat_id=profile.chat_id, text=text)
    await groupfilesend(chat_id=profile.chat_id, filename_list=profile.scans)


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = Executor.objects.all()
        profiles_list = [Profile(user) for user in users]
        asyncio.run(async_handle(profiles_list))
