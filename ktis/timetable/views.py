from django.shortcuts import get_object_or_404, render, redirect
from .models import User
from .forms import PostForm
import re
import time
from selenium import webdriver
from bs4 import BeautifulSoup


def index(request):
    token = str(time.time())
    request.session['token'] = token
    return redirect('account')


def account(request):
    token = request.session.get('token')
    user_list = User.objects.filter(token_text=token)
    return render(request, 'timetable/index.html', {'user_list': user_list})


def detail(request, username_text):
    token = request.session.get('token')
    user = get_object_or_404(User, token_text=token, username_text=username_text)
    return render(request, 'timetable/detail.html', {'user': user})


def post(request):
    token = request.session.get('token')
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = User(token_text=token, username_text=form.data['username_text'], pw_text=form.data['pw_text'])
            post.save()
            return redirect('account')
    else:
        form = PostForm()
    return render(request, 'timetable/forms.html', {'form': form})


def delete(request, username_text):
    token = request.session.get('token')
    user = User.objects.get(token_text=token, username_text=username_text)
    user.delete()
    return redirect('account')


def result(request):
    token = request.session.get('token')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    driver = webdriver.Chrome('/Users/simonkim/PycharmProjects/KTISparse/chromedriver', chrome_options=options)
    def parse_table(username, pw):
        driver.get('https://ktis.kookmin.ac.kr')

        input_element = driver.find_element_by_name("txt_user_id")
        input_element.send_keys(username)
        input_element = driver.find_element_by_name("txt_passwd")
        input_element.send_keys(pw)

        input_element.submit()

        driver.get('https://ktis.kookmin.ac.kr/kmu/usb.Usb0102rAGet01.do')

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        tables = soup.findAll("table")[1]

        tr_list = tables.select("tr")[8:]
        tr_list = tr_list[:-1]

        temp_list = list()

        for tr in tr_list:
            td = tr.select("td")[6]
            string = td.text.replace(", ", ",").replace("7호관", "칠호관")
            temp_list += string.split()

        final_list = list()

        eng_pattern = re.compile(r"[월,화,수,목,금,토][A-Z]")
        num_pattern = re.compile(r"[월,화,수,목,금,토]\d{1,2}")

        for i in temp_list:
            i = re.sub(",", i[0], i)
            match = eng_pattern.findall(i)
            final_list.extend(match)
            match = num_pattern.findall(i)
            final_list.extend(match)

        return final_list

    def processed_table(table_list):
        table_dic = {"0": ["08:00", "09:00"], "1": ["09:00", "10:00"], "2": ["10:00", "11:00"], "3": ["11:00", "12:00"],
                     "4": ["12:00", "13:00"], "5": ["13:00", "14:00"], "6": ["14:00", "15:00"], "7": ["15:00", "16:00"],
                     "8": ["16:00", "17:00"], "9": ["17:00", "18:00"], "10": ["18:00", "18:55"],
                     "11": ["18:55", "19:50"],
                     "12": ["19:50", "20:45"], "13": ["20:45", "21:40"], "14": ["21:40", "22:30"],
                     "A": ["09:00", "10:30"],
                     "B": ["10:30", "12:00"], "C": ["12:00", "13:30"], "D": ["13:30", "15:00"], "E": ["15:00", "16:30"],
                     "F": ["16:30", "18:00"], "G": ["18:00", "19:25"], "H": ["19:25", "20:50"], "I": ["20:50", "22:05"]}
        table_list = sorted(list(set(table_list)))
        mon = list()
        tue = list()
        wed = list()
        thu = list()
        fri = list()
        sat = list()
        for i in table_list:
            if i[0] == "월":
                mon.append(table_dic[i[1:]])
            elif i[0] == "화":
                tue.append(table_dic[i[1:]])
            elif i[0] == "수":
                wed.append(table_dic[i[1:]])
            elif i[0] == "목":
                thu.append(table_dic[i[1:]])
            elif i[0] == "금":
                fri.append(table_dic[i[1:]])
            elif i[0] == "토":
                sat.append(table_dic[i[1:]])

        return mon, tue, wed, thu, fri, sat

    def convert_json(mon, tue, wed, thu, fri, sat):
        def list_to_json(lists, date):
            out_list = str()
            for val in lists:
                out_list += time_to_json(val, date)
            return out_list


        def time_to_json(val, date):
            out_str = str()
            out_str += date
            out_str += "T"
            out_str += val[0]
            out_str += ":00"
            out_str += date
            out_str += "T"
            out_str += val[1]
            out_str += ":00"
            return out_str


        out_list = str()
        out_list += list_to_json(mon, '1970-01-05')
        out_list += list_to_json(tue, '1970-01-06')
        out_list += list_to_json(wed, '1970-01-07')
        out_list += list_to_json(thu, '1970-01-08')
        out_list += list_to_json(fri, '1970-01-09')
        out_list += list_to_json(sat, '1970-01-10')
        return out_list

    timetables = list()
    users = User.objects.filter(token_text=token)
    for i in users:
        timetables.extend(parse_table(i.username_text, i.pw_text))
    driver.quit()
    users.delete()

    mon, tue, wed, thu, fri, sat = processed_table(timetables)
    del timetables
    return render(request, 'timetable/result.html', {'result_json': convert_json(mon, tue, wed, thu, fri, sat)})