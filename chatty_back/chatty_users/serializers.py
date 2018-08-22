from rest_framework import serializers
from . import models


class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'id',
            'name',
            'unique_user_id',
        )


class NewUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'name',
            'unique_user_id',
        )
        extra_kwargs = {'name': {'required': True}}


