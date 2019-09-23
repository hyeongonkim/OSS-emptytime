from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class TitleData(models.Model):
    title = models.CharField(max_length=500)
    def __str__(self):
        return self.title
# class EmailAccount(models.Model):
#     myEmail = models.CharField(max_length=30)
#     def __str__(self):
#         return self.myEmail
class Mytag(models.Model):
    myTag = models.CharField(max_length=20)
    account=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.tag
