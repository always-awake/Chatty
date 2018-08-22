from django.utils.decorators import method_decorator
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
from . import models, serializers
from chatty_back.chatty_users import models as chattyuser_models
from chatty_back.partners import models as partners_models


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


class Startchat(APIView):

    """ 채팅을 처음 시작했을 때 """
    
    @method_decorator(check_user())
    def post(self, request, user, format=None):

        request_day = timezone.now().day
        
        try: 
            today_diary = models.Single_diary.objects.get(created_at__day=request_day)

            return Response(status=status.HTTP_401_UNAUTHORIZED)

        except models.Single_diary.DoesNotExist:

            #weather을 가져오기

            question_set = models.Question_set.objects.get(id=1)
            #
            serializer = serializers.DiarySerializer_store(data=request.data)

            if serializer.is_valid():
                
                user_partner = partner_models.Partner.objects.get(name=user.partner)

                new_diary_id = serializer.save(creator=user, question_set=question_set, partner=user_partner).id

                new_diary = models.Single_diary.objects.get(id=new_diary_id)
                    
                serializer = serializers.StartChatSerializer(new_diary)

                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                
            else:

                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
            