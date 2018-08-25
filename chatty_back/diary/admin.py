from django.contrib import admin
from . import models


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display =(
        'id',
        'message',
        'creator',
    )

@admin.register(models.Question_set)
class Question_setAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'question_list',
    )

@admin.register(models.Single_diary)
class Single_diaryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'state',
        'creator',
        'question_set',
        'created_at',
    )


@admin.register(models.User_answer)
class User_answerAdmin(admin.ModelAdmin):

    list_display = (
        'answer',
        'diary',
        'creator',
    )
