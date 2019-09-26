from django.shortcuts import get_object_or_404, render, redirect
from .models import User
from .forms import PostForm
import re
from selenium import webdriver
from bs4 import BeautifulSoup


def index(request):
    user_list = User.objects.order_by('username_text')
    return render(request, 'html/index.html', {'user_list': user_list})


def detail(request, username_text):
    user = get_object_or_404(User, username_text=username_text)
    return render(request, 'html/detail.html', {'user': user})


def post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = User(username_text=form.data['username_text'], pw_text=form.data['pw_text'])
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'html/forms.html', {'form': form})


def delete(request, username_text):
    user = User.objects.get(username_text=username_text)
    user.delete()
    return redirect('index')


def result(request):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
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
        def list_to_json(list):
            out_str = "["
            for val in list:
                out_str += time_to_json(val)
                out_str += ", "

            if len(out_str) > 2:
                out_str = out_str[:-2]

            out_str += "], "
            return out_str

        def time_to_json(val):
            out_str = "{\"start\":\""
            out_str += val[0]
            out_str += "\", \"end\":\""
            out_str += val[1]
            out_str += "\"}"
            return out_str

        out_str = "{"
        out_str += "\"mon\":"
        out_str += list_to_json(mon)
        out_str += "\"tue\":"
        out_str += list_to_json(tue)
        out_str += "\"wed\":"
        out_str += list_to_json(wed)
        out_str += "\"thu\":"
        out_str += list_to_json(thu)
        out_str += "\"fri\":"
        out_str += list_to_json(fri)
        out_str += "\"sat\":"
        out_str += list_to_json(sat)
        out_str = out_str[:-2]
        out_str += "}"
        return out_str

    timetables = list()
    users = User.objects.order_by('username_text')
    for i in users:
        timetables.extend(parse_table(i.username_text, i.pw_text))
    driver.quit()

    mon, tue, wed, thu, fri, sat = processed_table(timetables)
    del timetables
    return render(request, 'html/result.html', {'result_json': convert_json(mon, tue, wed, thu, fri, sat)})