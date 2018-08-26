from rest_framework import serializers
from . import models
from chatty_back.chatty_users import serializers as chattyuser_serializers
from chatty_back.chatty_users import models as chattyuser_models


class PartnerProfileSerializer(serializers.ModelSerializer):

    diary_count = serializers.ReadOnlyField()
    days_together = serializers.ReadOnlyField()
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = models.Partner
        fields = (
            'id',
            'profile_image',
            'name',
            'bio',
            'diary_count',
            'days_together',
            'created_at',
        )


class CreatePartnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Partner
        fields = (
            'profile_image',
            'name', 
            'bio',
        )
        extra_kwargs = {'name': {'required': True}}


class PartnerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Partner
        fields = (
            'id',
            'profile_image',
            'name',
            'created_at',
        )


class MainPartnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Partner
        fields = (
            'id',
            'name',
            'days_together',
            'diary_count',
        )