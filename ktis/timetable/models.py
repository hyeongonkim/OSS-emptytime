from django.db import models


class User(models.Model):
    username_text = models.CharField(max_length=8)
    pw_text = models.CharField(max_length=30)

    def __str__(self):
        return self.username_text