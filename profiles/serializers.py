from rest_framework import serializers
from .models import Profile, Interest
from followers.models import Follower


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    preferences = serializers.StringRelatedField(many=True)
    following_id = serializers.SerializerMethodField()
    events_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            print(following)
            return following.id if following else None
        return None

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'preferences',
            'name', 'content', 'image', 'is_owner', 'following_id',
            'events_count', 'followers_count', 'following_count'
        ]


class InterestSerializer(serializers.ModelSerializer):
    profile = serializers.ReadOnlyField(source='profile.owner.username')
    is_owner = serializers.SerializerMethodField()
    genre_name = serializers.SerializerMethodField()

    def get_genre_name(self, obj):
        return obj.genre.gen_name

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.profile.owner

    class Meta:
        model = Interest
        fields = [
            'id', 'profile', 'genre', 'genre_name', 'is_owner'
        ]
