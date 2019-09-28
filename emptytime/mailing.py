import requests
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emptytime.settings")
import django
django.setup()
from notice.models import Mytag,  RecentTitle
from django.contrib.auth.models import User

def search():
    user_list = []
    for userName in User.objects.all():
        user_list.append(userName.username)

    for user in user_list:
        user_tag_list = []
        for user_tag in Mytag.object.filter(account__username=user):
            user_tag_list.append(user_tag.myTag)




