from rest_framework import serializers
from . import models
from chatty_back.chatty_users import serializers as chattyuser_serializers



class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Question
        fields = (
            'id',
            'message',
            #질문 내용과 질문 id를 보여줌
        )


class Question_setSerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(many=True)

    class Meta:
        model = models.Question_set
        fields = (
            'questions',
        )


class DiarySerializer_store(serializers.ModelSerializer):

    class Meta:
        model = models.Single_diary
        fields = (
        )


class DiarySerializer_view(serializers.ModelSerializer):
    
    current_question = QuestionSerializer()

    class Meta:
        model = models.Single_diary
        fields = (
            'id',
            'current_question',          
        )


#answer 저장을 위한 시리얼라이즈
class AnswerSerializer_store(serializers.ModelSerializer):

    class Meta:
        model = models.User_answer
        fields = (
            'id',
            'answer',
        )

       
#answer json화를 위한 시리얼라이즈
class AnswerSerializer_view(serializers.ModelSerializer):

    class Meta:
        model = models.User_answer
        fields = (
            'question',
            'answer',
            'image',
            'created_at',
        )


class MainAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User_answer
        fields = (
            'answer',
        )


class DiaryDetailSerializer(serializers.ModelSerializer):

    answers = AnswerSerializer_view(many=True)
    questions = QuestionSerializer(many=True)

    class Meta:
        model = models.Single_diary
        fields = (
            'questions',
            'answers',
            'created_at',
        )


class CalendarSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Single_diary
        fields = (
            'id',
            'created_at',
        )


class LastAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Single_diary
        fields = (
            'last_answer',
        )


class StartChatSerializer(serializers.ModelSerializer):

    question = QuestionSerializer()

    class Meta:
        model = models.Single_diary
        fields = (
            'id',
            'question',
        )


class MainDiarySerializer(serializers.ModelSerializer):
    
    answer = MainAnswerSerializer()

    class Meta:
        model = models.Single_diary
        fields = (
            'id',
            'image',
            'created_at',
            'answer'
        )