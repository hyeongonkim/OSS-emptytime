import requests
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emptytime.settings")
import django
django.setup()
from notice.models import Mytag,  TitleData, KmTitle
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
            latestSWNotice =TitleData.objects.first()
            latestKMNotice =KmTitle.objects.first()
            SWkeyword=latestSWNotice.title
            KMkeyword=latestKMNotice.km_title
            if word in SWkeyword:
                email = EmailMessage("'"+word+"'"+'(이)가 포함된 학부공지사항이 올라왔습니다.',
                                     'https://cs.kookmin.ac.kr/news/notice/'+str(latestSWNotice.link),
                                     to=[User.objects.get(username=user).email])
                email.send()
            if word in KMkeyword:
                email = EmailMessage("'" + word + "'" + '(이)가 포함된 국민대공지사항이 올라왔습니다.',
                                     'https://cs.kookmin.ac.kr/news/notice/' + str(latestKMNotice.km_link),
                                     to=[User.objects.get(username=user).email])
                email.send()

if __name__=='__main__':
    search()






