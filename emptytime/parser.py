import requests
from bs4 import BeautifulSoup
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emptytime.settings")
import django
django.setup()
# HTTP GET Request
from notice.models import TitleData, KmTitle
prev_fist_sw=TitleData.objects.first()
prev_fist_km=KmTitle.objects.first()

TitleData.objects.all().delete()
KmTitle.objects.all().delete()
def parse():
    list = {}
    for num in range((TitleData.objects.first().link)+1, (TitleData.objects.first().link)-20,-1):
        code=str(num)
        req = requests.get('https://cs.kookmin.ac.kr/news/notice/'+code)
        # HTML 소스 가져오기

        html = req.text
        # BeautifulSoup으로 html소스를 python객체로 변환하기
        # 첫 인자는 html소스코드, 두 번째 인자는 어떤 parser를 이용할지 명시.
        # 이 글에서는 Python 내장 html.parser를 이용했다.
        soup = BeautifulSoup(html, 'html.parser')

        my_title = soup.find("td",{"class": "view-title"})
        if my_title == None:
            continue

        list[my_title.text] = num
    return list
def parse_km():

    req = requests.get('https://www.kookmin.ac.kr/site/ecampus/notice/all/')
    # HTML 소스 가져오기

    html = req.content.decode('utf-8')
    # BeautifulSoup으로 html소스를 python객체로 변환하기
    # 첫 인자는 html소스코드, 두 번째 인자는 어떤 parser를 이용할지 명시.
    # 이 글에서는 Python 내장 html.parser를 이용했다.
    soup = BeautifulSoup(html, 'html.parser')

    my_title = soup.select(
        '#content_body > section > div.boardlist > table > tbody > tr > td > a'
        )
    km_list = {}
    for title in my_title:
        km_list[title.text] = title.get('href')[2:]



    return km_list
if __name__=='__main__':
    prev_fist_km.save()
    prev_fist_sw.save()
    blog_data_list= parse()
    km_data_list=parse_km()

    for key, value in blog_data_list.items():
        TitleData(title=key,link=value).save()

    for key, value in km_data_list.items():

        KmTitle(km_title=key,km_link=value).save()

    prev_fist_sw.delete()
    prev_fist_km.delete()

