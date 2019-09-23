from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home , name='home' ),
    path('empty/', views.empty, name='empty'),
    path('email/', views.email, name='email'),
    path('email_control', views.email_control, name='control'),
    path('join/', views.signup, name= 'join'),
    path('login/', views.signin, name='login'),
    path('addTag/', views.addTag, name='addTag'),
]