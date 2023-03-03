from rest_framework import serializers
from .models import Event, Gallery, Photo, EventGenre
from categories.models import Category
from buttons.models import Interested, Going


class EventSerializer(serializers.ModelSerializer):
    event_genres = serializers.StringRelatedField(many=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField()
    interested_id = serializers.SerializerMethodField()
    interested_count = serializers.ReadOnlyField()
    goings_id = serializers.SerializerMethodField()
    goings_count = serializers.ReadOnlyField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_interested_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            interested = Interested.objects.filter(
                owner=user, posted_event=obj
            ).first()
            return interested.id if interested else None
        return None

    def get_goings_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            goings = Going.objects.filter(
                owner=user, posted_event=obj
            ).first()
            return goings.id if goings else None
        return None

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'This event already exists!'
            })

    class Meta:
        model = Event
        fields = [
            'id', 'owner', 'category', 'title', 'date',
            'location', 'address', 'created_at', 'updated_at',
            'content', 'image', 'is_owner', 'event_genres',
            'comments_count', 'interested_id', 'interested_count',
            'goings_id', 'goings_count',
            'profile_id', 'profile_image'
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
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'image size larger than 2MB!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'image width larger than 4094px!'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'image height larger than 4094px!'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Photo
        fields = [
            'id', 'gallery', 'owner', 'title',
            'created_at', 'image', 'is_owner',
            'profile_id', 'profile_image'
        ]


class PhotoDetailSerializer(PhotoSerializer):
    """
    Serializer for the EventGenre model used in Detail view
    event is a read only field so that we dont have to set it on each update
    """
    gallery = serializers.ReadOnlyField(source='gallery.id')


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

    def validate(self, value):
        print("VALUE", value)
        if value['event'].category != value['genre'].category:
            raise serializers.ValidationError(
                'The event catogory and its genre category must match'
            )
        return value

    class Meta:
        model = EventGenre
        fields = [
            'id', 'event', 'genre',
            'event_title', 'genre_name',
            'genre_category', 'event_category'
        ]


class EventGenreDetailSerializer(EventGenreSerializer):
    """
    Serializer for the EventGenre model used in Detail view
    event is a read only field so that we dont have to set it on each update
    """
    event = serializers.ReadOnlyField(source='event.id')
