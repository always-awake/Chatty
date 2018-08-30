from django.urls import path
from . import views

app_name = "diary"
urlpatterns = [
    path('main/', views.MainDiary.as_view(), name='main diaries module'),
    path('startchat/', views.Startchat.as_view(), name='start chat'),
    path('chat/<int:diary_id>/', views.Chat.as_view(), name='chat'),
    path('feeling/<int:diary_id>', views.Feeling.as_view(), name='feeling'),
    path('detail/<int:diary_id>/', views.DiaryDetail.as_view(), name='diary detail'),
    path('calendar/', views.ThisMonth_Calendar.as_view(), name='this month calendar'),
    path('calendar/<int:month>/', views.OtherMonth_Calendar.as_view(), name='other month calendar'),
    path('question/', views.Question.as_view(), name='add question & delete question'),
    path('question/list/', views.QuestionList.as_view(), name='list question'),

    path('question_set/', views.CreateQuestionSet.as_view(), name='question_set'),
]