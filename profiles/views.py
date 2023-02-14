from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, permissions
from .models import Profile, Interest
from .serializers import ProfileSerializer, InterestSerializer
from drf_api_event.permissions import IsOwnerOrReadOnly
from drf_api_event.permissions import IsProfileOwnerOrReadOnly


class ProfileList(generics.ListCreateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class ProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class InterestList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = InterestSerializer
    queryset = Interest.objects.all()

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class InterestDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsProfileOwnerOrReadOnly]
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
