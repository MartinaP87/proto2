from rest_framework import serializers
from .models import Event, Gallery, Photo, EventGenre
from categories.models import Category


class EventSerializer(serializers.ModelSerializer):
    event_genres = serializers.StringRelatedField(many=True)
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
            'content', 'image', 'is_owner',
            'event_genres'
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


class EventGenreSerializer(serializers.ModelSerializer):
    event_title = serializers.SerializerMethodField()
    genre_name = serializers.SerializerMethodField()
    genre_category = serializers.SerializerMethodField()
    event_category = serializers.SerializerMethodField()

    def get_event_title(self, obj):
        return obj.event.title

    def get_genre_name(self, obj):
        return obj.genre.gen_name

    def get_genre_category(self, obj):
        return obj.genre.category.cat_name

    def get_event_category(self, obj):
        return obj.event.category.cat_name

    class Meta:
        model = EventGenre
        fields = [
            'id', 'event', 'genre',
            'event_title', 'genre_name',
            'genre_category', 'event_category'
        ]
