from rest_framework import serializers
from django.db import IntegrityError
from .models import Interested, Going, Like


class InterestedSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Interested
        fields = [
            'id', 'owner', 'posted_event', 'created_at',
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })


class GoingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    event_name = serializers.SerializerMethodField()

    def get_event_name(self, obj):
        return obj.posted_event.title

    class Meta:
        model = Going
        fields = [
            'id', 'owner', 'posted_event', 'event_name',
            'created_at'
            
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField()

    class Meta:
        model = Like
        fields = [
            'id', 'owner', 'comment', 'created_at'
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })
