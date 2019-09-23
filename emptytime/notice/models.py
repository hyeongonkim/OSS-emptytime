from django.db import models

# Create your models here.
class TitleData(models.Model):
    title = models.CharField(max_length=500)
    def __str__(self):
        return self.title
class EmailAccount(models.Model):
    myEmail = models.CharField(max_length=50)
    def __str__(self):
        return self.myEmail
class Mytag():
    tag = models.CharField(max_length=50)
    emailAccount=models.ForeignKey(EmailAccount,on_delete=models.CASCADE)
    def __str__(self):
        return self.tag
