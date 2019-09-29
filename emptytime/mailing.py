import requests
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emptytime.settings")
import django
django.setup()
from notice.models import Mytag,  RecentTitle
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
def search():
    user_list = []
    for userName in User.objects.all():
        user_list.append(userName.username)

    for user in user_list:
        user_tag_list = []
        for user_tag in Mytag.objects.filter(account__username=user):
            user_tag_list.append(user_tag.myTag)
        for word in user_tag_list:
            keyword=RecentTitle.objects.filter(recent_SW_notie__icontains=word)
            if keyword.count() !=0:
                email = EmailMessage(user, word, to=[User.objects.get(username=user).email])
                email.send()

if __name__=='__main__':
    search()






