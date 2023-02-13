from rest_framework import serializers
from .models import Event, Gallery, Photo
from categories.models import Category


class EventSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Event
        fields = [
            'id', 'owner', 'category', 'title', 'date',
            'location', 'address', 'created_at', 'updated_at',
            'content', 'image', 'is_owner'
        ]


class GallerySerializer(serializers.ModelSerializer):
    posted_event = serializers.ReadOnlyField(source='posted_event.title')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.posted_event.owner

    class Meta:
        model = Gallery
        fields = [
            'id', 'posted_event', 'name', 'is_owner'
        ]


class PhotoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    gallery = serializers.ReadOnlyField(source='gallery.name')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Photo
        fields = [
            'id', 'gallery', 'owner', 'title',
            'created_at', 'image', 'is_owner'
        ]
