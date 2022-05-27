from django.core.management.base import BaseCommand

from telebot.bot_executor import app_executor


class Command(BaseCommand):
    def handle(self, *args, **options):
        app_executor.run_polling()
