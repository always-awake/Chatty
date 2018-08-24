from django.urls import path
from . import views

app_name = "diary"
urlpatterns = [
    path('startchat/', views.Startchat.as_view(), name='start chat'),
    path('chat/<int:diary_id>/', views.Chat.as_view(), name='chat'),
    path('detail/<int:diary_id>/', views.DiaryDetail.as_view(), name='diary detail'),
    path('calendar/', views.ThisMonth_Calendar.as_view(), name='this month calendar'),
    path('calendar/<int:month>/', views.OtherMonth_Calendar.as_view(), name='other month calendar'),
    path('question/', views.AddQuestion.as_view(), name='add question'),
]