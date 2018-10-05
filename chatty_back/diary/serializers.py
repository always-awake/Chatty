from rest_framework import serializers
from . import models
from chatty_back.chatty_users import serializers as chattyuser_serializers
from chatty_back.partners import serializers as partners_serializers


class QuestionSerializer(serializers.ModelSerializer):

    question_id = serializers.IntegerField(source='id')

    class Meta:
        model = models.Question
        fields = (
            'question_id',
            'message',
            #질문 내용과 질문 id를 보여줌
        )
        extra_kwargs = {'message': {'required': True}}

class Question_setSerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(many=True)

    class Meta:
        model = models.Question_set
        fields = (
            'questions',
        )


#answer 저장을 위한 시리얼라이즈
class AnswerSerializer_store(serializers.ModelSerializer):

    class Meta:
        model = models.User_answer
        fields = (
            'image',
            'label',
        )

       
#answer json화를 위한 시리얼라이즈
class AnswerSerializer_view(serializers.ModelSerializer):

    class Meta:
        model = models.User_answer
        fields = (
            'question',
            'label',
            'image',
            'created_at',
        )


class MainAnswerSerializer(serializers.ModelSerializer):

    answer_id = serializers.IntegerField(source='id')

    class Meta:
        model = models.User_answer
        fields = (
            'answer_id',
            'image',
            'label',
        )


class DiarySerializer_view(serializers.ModelSerializer):
    
    current_question = QuestionSerializer()
    diary_id = serializers.IntegerField(source='id')
    
    class Meta:
        model = models.Single_diary
        fields = (
            'diary_id',
            'current_question',          
        )


class DiaryDetailSerializer(serializers.ModelSerializer):

    answers = AnswerSerializer_view(many=True)
    questions = QuestionSerializer(many=True)
    diary_id = serializers.IntegerField(source='id')
    partner = partners_serializers.DiaryDetailSerializer()
    
    class Meta:
        model = models.Single_diary
        fields = (
            'partner',
            'diary_id',
            'weather',
            'feeling',
            'questions',
            'answers',
            'created_at',
        )


class CalendarSerializer(serializers.ModelSerializer):

    diary_id = serializers.IntegerField(source='id')

    class Meta:
        model = models.Single_diary
        fields = (
            'diary_id',
            'created_at',
        )


class LastAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Single_diary
        fields = (
            'answers',
        )


class StartChatSerializer(serializers.ModelSerializer):

    question = QuestionSerializer()
    diary_id = serializers.IntegerField(source='id')

    class Meta:
        model = models.Single_diary
        fields = (
            'diary_id',
            'question',
        )


class MainDiarySerializer(serializers.ModelSerializer):
    
    answers = MainAnswerSerializer(many=True)
    diary_id = serializers.IntegerField(source='id')

    class Meta:
        model = models.Single_diary
        fields = (
            'diary_id',
            'created_at',
            'answers',
            #main_image',
        )


class FeelingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Single_diary
        fields = (
            'feeling',
        )

## 임시 APi
class QS_Serializer(serializers.ModelSerializer):

    class Meta:
        model = models.Question_set
        fields = (
            'question_list',
        )