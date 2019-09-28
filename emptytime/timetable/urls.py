from django.urls import path

from . import views

app_name='timetable'

urlpatterns = [
    path('', views.index, name='index'),
    path('account/', views.account, name='account'),
    path('account/add/', views.post, name='adduser'),
    path('account/result/', views.result, name='result'),
    path('account/delete/<str:username_text>/', views.delete, name='delete'),
]