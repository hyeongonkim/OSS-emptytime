from django.urls import path

from . import views

app_name='timetable'

urlpatterns = [
    path('', views.index, name='index'),
    path('account/', views.account, name='account'),
    path('account/add/', views.post, name='adduser'),
    path('account/result/', views.result, name='result'),
    path('account/<str:username_text>/', views.detail, name='detail'),
    path('account/<str:username_text>/delete/', views.delete, name='delete'),
]