import asyncio

from django.db import models

# Create your models here.
from telebot.bot_src.shared import UPLOAD_PATH


class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Executor(models.Model):
    user_id = models.PositiveBigIntegerField(unique=True)
    chat_id = models.PositiveBigIntegerField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    photo = models.FilePathField(path=UPLOAD_PATH, blank=True, null=True)
    category = models.ManyToManyField(Category)
    lang_level = models.CharField(max_length=50)
    approved = models.BooleanField(default=False)
    welcome_sended = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user_id)

    def save(self, *args, **kwargs):
        from telebot.bot_src.triggers import executor_approved
        if self.approved and not self.welcome_sended:
            asyncio.run(executor_approved(self.chat_id))
            self.welcome_sended = True
        super(Executor, self).save(*args, **kwargs)


class Certificate(models.Model):
    file = models.FilePathField(path=UPLOAD_PATH)
    executor = models.ForeignKey(Executor, on_delete=models.CASCADE)

    def __str__(self):
        return self.file


class Client(models.Model):
    user_id = models.PositiveBigIntegerField(unique=True)
    chat_id = models.PositiveBigIntegerField(unique=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.user_id)


class ClientRequest(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    problem = models.TextField()
    budget = models.IntegerField()
    sended = models.BooleanField(default=False)

    def __str__(self):
        return self.problem

    def save(self, *args, **kwargs):
        super(ClientRequest, self).save(*args, **kwargs)
        if not self.sended:
            from telebot.bot_src.triggers import send_request_to_all_executors
            # asyncio.run(executor_approved(self.chat_id))
            send_request_to_all_executors(self)
            self.sended = True
            # super(ClientRequest, self).save(*args, **kwargs)
            self.save()

class Session(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    executor = models.ForeignKey(Executor, on_delete=models.CASCADE)
    request = models.ForeignKey(ClientRequest, on_delete=models.CASCADE)
    date_time = models.DateTimeField()

    def __str__(self):
        return f'{self.client} - {self.executor}: {self.date_time}'
