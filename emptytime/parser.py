import requests
from bs4 import BeautifulSoup
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emptytime.settings")
import django
django.setup()
# HTTP GET Request
from notice.models import TitleData
def parse():
    list = []
    for num in range(2560, 2581):
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
        list.append(my_title.text)
    return list

if __name__=='__main__':
    blog_data_list= parse()
    for t in blog_data_list:
        TitleData(title=t).save()