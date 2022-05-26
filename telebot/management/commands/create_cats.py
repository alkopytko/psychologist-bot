from django.core.management.base import BaseCommand

from telebot.bot_src.executor.signup_vars import Categories
from telebot.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        for cat in Categories.categories:
            Category.objects.get_or_create(category=cat)
