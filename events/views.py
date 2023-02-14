from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from drf_api_event.permissions import IsOwnerOrReadOnly, IsEventOwnerOrReadOnly
from drf_api_event.permissions import IsGalleryOwnerOrReadOnly
from .models import Event, Gallery, Photo, EventGenre
from .serializers import EventSerializer, GallerySerializer, PhotoSerializer
from .serializers import EventGenreSerializer


class EventList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class GalleryList(generics.ListAPIView):
    serializer_class = GallerySerializer
    queryset = Gallery.objects.all()


class GalleryDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsGalleryOwnerOrReadOnly]
    serializer_class = GallerySerializer
    queryset = Gallery.objects.all()


class PhotoList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()


class EventGenreList(generics.ListCreateAPIView):
    serializer_class = EventGenreSerializer
    queryset = EventGenre.objects.all()
    print('QUERY', queryset[0].event.category)
    print('QUERY2', queryset[0].genre.category)

    def perform_create(self, serializer):
        if serializer.validated_data[
        'event'].category == serializer.validated_data['genre'].category:
            serializer.save()
        else:
            serializer.save()


class EventGenreDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsEventOwnerOrReadOnly]
    serializer_class = EventGenreSerializer
    queryset = EventGenre.objects.all()
