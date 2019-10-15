import requests
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emptytime.settings")
import django
django.setup()
from notice.models import Mytag,  TitleData, KmTitle, RecentTagLink
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
latestSWNotice =TitleData.objects.first()
latestKMNotice =KmTitle.objects.first()
SWkeyword=latestSWNotice.title
KMkeyword=latestKMNotice.km_title
def search():
    user_list = []
    for userName in User.objects.all():
        user_list.append(userName.username)

    for user in user_list:
        user_tag_list = []
        for user_tag in Mytag.objects.filter(account__username=user):
            user_tag_list.append(user_tag.myTag)
        for word in user_tag_list:

            if RecentTagLink.objects.first().sw_link != latestSWNotice.link:
                if word in SWkeyword:
                    email = EmailMessage("'"+word+"'"+'(이)가 포함된 소융대 공지사항이 올라왔습니다.',
                                         latestSWNotice.title +'\n'+
                                         'https://cs.kookmin.ac.kr/news/notice/'+str(latestSWNotice.link) +'\n\n'+
                                         '- 이 메일은 TimePush 서비스를 통해 자동으로 발송되었습니다.',
                                         to=[User.objects.get(username=user).email])
                    email.send()
            if RecentTagLink.objects.first().km_link != latestKMNotice.km_link:
                if word in KMkeyword:
                    email = EmailMessage("'" + word + "'" + '(이)가 포함된 국민대 공지사항이 올라왔습니다.',
                                         latestKMNotice.km_title + '\n' +
                                         'https://www.kookmin.ac.kr/site/ecampus/notice/all/'+ str(latestKMNotice.km_link) +'\n\n'+
                                         '- 이 메일은 TimePush 서비스를 통해 자동으로 발송되었습니다.',
                                         to=[User.objects.get(username=user).email])
                    email.send()

if __name__=='__main__':
    if RecentTagLink.objects.first().sw_link != latestSWNotice.link:
        search()
        temp = RecentTagLink.objects.first()
        temp.sw_link = TitleData.objects.first().link
        temp.save()
    if RecentTagLink.objects.first().km_link != latestKMNotice.km_link:
        search()
        temp = RecentTagLink.objects.first()
        temp.km_link = KmTitle.objects.first().km_link
        temp.save()







