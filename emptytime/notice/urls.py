from django.urls import path
from . import views
app_name='notice'
urlpatterns = [
    path('', views.home , name='home'),
    path('email/', views.email, name='email'),
    path('email_control/', views.email_control, name='control'),
    path('agree/', views.agree, name='agree'),
    path('join/', views.signup, name= 'join'),
    path('login/', views.signin, name='login'),
    path('logout/', views.logout, name='logout'),
    path('addTag/', views.addTag, name='addTag'),
    path('delTag/<int:tag_id>',views.delTag, name = 'delTag'),
]