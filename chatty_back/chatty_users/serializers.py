from rest_framework import serializers
from . import models


class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ChattyUser
        fields = (
            'id',
            'name',
            'unique_user_id',
        )


class NewUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ChattyUser
        fields = (
            'name',
            'unique_user_id',
        )
        extra_kwargs = {'name': {'required': True}}


