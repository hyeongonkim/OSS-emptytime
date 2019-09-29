from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class TitleData(models.Model):
    title = models.CharField(max_length=500)
    link = models.IntegerField()
    def __str__(self):
        return self.title
class Mytag(models.Model):
    myTag = models.CharField(max_length=20)
    account=models.ForeignKey(User,on_delete=models.CASCADE, default='1')
    def __str__(self):
        return self.myTag
class KmTitle(models.Model):
    km_title = models.CharField(max_length=500)
    km_link = models.IntegerField()
    def __str__(self):
        return self.km_title