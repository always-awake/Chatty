from django.urls import path
from . import views


app_name = "chatty_users"
urlpatterns = [
    path('', views.Main.as_view(), name='diary feed'),
    path("newuser/", views.NewUser.as_view(), name='first login user'), #hash값 처음으로 반환
]
