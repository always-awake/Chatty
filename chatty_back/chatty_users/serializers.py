from rest_framework import serializers
from chatty_back.partners import serializers as partners_serializers
from chatty_back.diary.serializers import MainDiarySerializer
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


class MainSerializer(serializers.ModelSerializer):

    partner = partners_serializers.MainPartnerSerializer()
    diaries = MainDiarySerializer(many=True)

    class Meta:
        model = models.ChattyUser
        fields = (
            'partner',
            'diaries'
        )


class PartnerListSerializer(serializers.ModelSerializer):

    partners = partners_serializers.PartnerListSerializer(many=True)

    class Meta:
        model = models.ChattyUser
        fields = (
            'partners',
        )