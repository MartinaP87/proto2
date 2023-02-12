from rest_framework import serializers
from .models import Profile, Interest


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at',
            'name', 'content', 'image'
        ]


class InterestSerializer(serializers.ModelSerializer):
    profile = serializers.ReadOnlyField(source='profile.owner.username')
    genre = serializers.ReadOnlyField(source='genre.gen_name')

    class Meta:
        model = Interest
        fields = [
            'id', 'profile', 'genre'
        ]
