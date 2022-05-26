from django.core.management.base import BaseCommand

from telebot.bots import app_client


class Command(BaseCommand):
    def handle(self, *args, **options):
        app_client.run_polling()
