from django.utils.crypto import get_random_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers


class NewUser(APIView):

    def post(self, request, format=None):

        request_unique_user_id = request.META.get('HTTP_HASH', None)
        
        try:
            request_user = models.ChattyUser.objects.get(unique_user_id=request_unique_user_id)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except models.ChattyUser.DoesNotExist:

            new_unique_user_id = get_random_string(length=40)

            try:
                not_unique_user_hash = models.ChattyUser.objects.get(unique_user_id=new_unique_user_id)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except models.ChattyUser.DoesNotExist:
                serializer = serializers.NewUserSerializer(data=request.data)

                if serializer.is_valid():

                    serializer.save(unique_user_id=new_unique_user_id)

                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                
                else:

                    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)