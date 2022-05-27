from django.core.management.base import BaseCommand

from telebot.bot_client import app_client


class Command(BaseCommand):
    def handle(self, *args, **options):
        app_client.run_polling()
