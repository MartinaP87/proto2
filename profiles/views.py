from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, permissions, filters
from django.db.models import Count
from .models import Profile, Interest
from .serializers import ProfileSerializer, InterestSerializer
from drf_api_event.permissions import IsOwnerOrReadOnly
from drf_api_event.permissions import IsProfileOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        events_count=Count('owner__event', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter
    ]
    orderin_fields = [
        'events_count',
        'followers_count',
        'following_count'
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        events_count=Count('owner__event', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer


class InterestList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = InterestSerializer
    queryset = Interest.objects.all()

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class InterestDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsProfileOwnerOrReadOnly]
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
