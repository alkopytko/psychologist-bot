from django.db import models


# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=100)


class Executor(models.Model):
    user_id = models.PositiveBigIntegerField(unique=True)
    chat_id = models.PositiveBigIntegerField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    photo = models.FilePathField(blank=True, null=True)
    category = models.ManyToManyField(Category)
    lang_level = models.CharField(max_length=50)
    approved = models.BooleanField(default=False)
    welcome_sended = models.BooleanField(default=False)


class Certificate(models.Model):
    file = models.FilePathField()
    executor = models.ForeignKey(Executor, on_delete=models.CASCADE)


class Client(models.Model):
    user_id = models.PositiveBigIntegerField(unique=True)
    chat_id = models.PositiveBigIntegerField(unique=True)
    name = models.CharField(max_length=50, blank=True, null=True)


class ClientRequest(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    problem = models.TextField()
    budget = models.IntegerField()


class Session(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    executor = models.ForeignKey(Executor, on_delete=models.CASCADE)
    request = models.ForeignKey(ClientRequest, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
