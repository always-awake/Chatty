from django.utils.decorators import method_decorator
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
from chatty_back.chatty_users import models as chattyuser_models
from chatty_back.partners import models as partners_models
from . import models, serializers
import requests
import json


# request 유저가 회원가입이 되어 있는 유저인지 확인하는 함수
def check_user():
    def decorator(func):
        def wrapper(request, *args, **kwargs):

            request_unique_user_id = request.META.get('HTTP_HASH', None)

            try:
                user = chattyuser_models.ChattyUser.objects.get(unique_user_id=request_unique_user_id)
                return func(request, user, *args, **kwargs)

            except chattyuser_models.ChattyUser.DoesNotExist:
                raise Exception("Needs login")   

        return wrapper
    return decorator


# 처음 일기를 작성할 때 자동으로 날씨 정보를 가져오는 함수
def get_weather(self, city):

    api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=63321e5f0464f10f168bb0d73ad4512b&q='

    url = api_address + city
    
    response = requests.get(url)
    
    response_json = response.json()

    weather = response_json['weather'][0]['main']

    return weather


class Startchat(APIView):

    """ 채팅을 처음 시작했을 때 """

    @method_decorator(check_user())
    def post(self, request, user, format=None):

        request_day = timezone.now().day
        
        try: 
            today_diary = models.Single_diary.objects.get(created_at__day=request_day)
            return Response(status=status.HTTP_401_UNAUTHORIZED) # 이미 당일 작성한 일기가 있을 경우, 재작성 불가능

        except models.Single_diary.DoesNotExist:

            weather = get_weather(self, 'Seoul')

            question_set = models.Question_set.objects.get(id=1) # 테스트 -> 이후에 랜덤 추출로 변경 필요

            new_diary = models.Single_diary.objects.create(creator=user, question_set=question_set, partner=user.partner, weather=weather)

            new_diary.save()

            serializer = serializers.StartChatSerializer(new_diary)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            

class Chat(APIView):

    """ 처음 채팅 시작 이후 채팅 """

    @method_decorator(check_user())
    def post(self, requset, user, diary_id, format=None):
       
        try:
            diary = models.Single_diary.objects.get(creator=user, id=diary_id)
        except models.Single_diary.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        current_question = diary.current_question

        if current_question==None:           

            return Response(data=None, status=status.HTTP_404_NOT_FOUND)
        
        else:

            serializer = serializers.AnswerSerializer_store(data=requset.data)

            if serializer.is_valid():
                
                serializer.save(diary=diary, creator=user, question=current_question)

                diary.state = 'ongoing'
                
                diary.save()

                next_question = diary.current_question

                if next_question == None:

                    diary.state = 'complete'

                    diary.save()

                    return Response(None, status=status.HTTP_204_NO_CONTENT)
                
                else:
                    serializer = serializers.QuestionSerializer(next_question)

                    return Response(data=serializer.data, status=status.HTTP_200_OK)
            
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Feeling(APIView):

    """ feeling """

    @method_decorator(check_user())
    def put(self, request, user, diary_id, format=None):

        try:
            diary = models.Single_diary.objects.get(creator=user, id=diary_id, state='complete')
        except models.Single_diary.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = serializers.FeelingSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()
            
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DiaryDetail(APIView):

    """ 다이어리 상세보기 """

    @method_decorator(check_user())
    def get(self, request, user, diary_id, format=None):
        
        user_diary = models.Single_diary.objects.get(id=diary_id, creator=user, state='complete')
        
        serializer = serializers.DiaryDetailSerializer(user_diary)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    
class ThisMonth_Calendar(APIView):

    """ request가 이루어진 달의 달력 """

    @method_decorator(check_user())
    def get(self, request, user, format=None):

        request_month = timezone.now().month

        user_diaries = models.Single_diary.objects.filter(
            creator=user, created_at__month=request_month
            )

        serializer = serializers.CalendarSerializer(user_diaries, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class OtherMonth_Calendar(APIView):

    """ request가 이루어진 달 외의 달력 """

    @method_decorator(check_user())
    def get(self, request, user, month, format=None):
        
        user_diaries = models.Single_diary.objects.filter(
            creator=user, created_at__month=month
        )

        serializer = serializers.CalendarSerializer(user_diaries, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class Question(APIView):

    """ Add Question """

    @method_decorator(check_user())
    def post(self, request, user, format=None):

        serializer = serializers.QuestionSerializer(data=request.data, partial=True)

        if serializer.is_valid():

            serializer.save(creator=user)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionList(APIView):

    """ Question List """

    @method_decorator(check_user())
    def get(self, request, user, format=None):

        user_question = models.Question.objects.filter(creator=user)

        serializer = serializers.QuestionSerializer(user_question, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class Diary_Main(APIView):

    @method_decorator(check_user())
    def get(self, request, user, format=None):

        user_diaries = models.Single_diary.objects.filter(creator=user, state='complete')

        if user_diaries is None:

            return Response(status=status.HTTP_404_NOT_FOUND)

        else:

            serializer = serializers.MainDiarySerializer(user_diaries, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)


#임시 API
class CreateQuestionSet(APIView):

    @method_decorator(check_user())
    def post(self, request, user, format=None):

        serializer = serializers.QS_Serializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
