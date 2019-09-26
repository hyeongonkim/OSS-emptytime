from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.post, name='adduser'),
    path('result/', views.result, name='result'),
    path('<str:username_text>/', views.detail, name='detail'),
    path('<str:username_text>/delete/', views.delete, name='delete'),
]