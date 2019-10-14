from django.urls import path

from . import views

app_name='timetable'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('clearUser/', views.branchHome, name='branch'),
    path('agree/', views.agree, name='agree'),
    path('account/', views.account, name='account'),
    path('account/add/', views.post, name='adduser'),
    path('account/result/', views.result, name='result'),
    path('account/error/', views.error, name='error'),
    path('account/delete/<str:username_text>/', views.delete, name='delete'),
]