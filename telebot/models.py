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
    approved = models.BooleanField(default=False)
    welcome_sended=models.BooleanField(default=False)

class Certificate(models.Model):
    file=models.FilePathField()
    executor=models.ForeignKey(Executor,on_delete=models.CASCADE)
