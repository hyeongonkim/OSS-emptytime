from django.shortcuts import render
from . models import TitleData
# Create your views here.
def home(request):
    return render(request, 'notice/home.html')


def email(request):
    context = {
        'notice_list': TitleData.objects.all(),
    }
    return render(request, 'notice/email.html', context)

def empty(request):
    return render(request, 'notice/empty.html')


def email_control(request):
    return render(request, 'notice/email_service_control.html')