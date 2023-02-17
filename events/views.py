from django.shortcuts import render
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import status, generics, permissions, filters
from drf_api_event.permissions import IsOwnerOrReadOnly, IsEventOwnerOrReadOnly
from drf_api_event.permissions import IsGalleryOwnerOrReadOnly
from .models import Event, Gallery, Photo, EventGenre
from .serializers import EventSerializer, GallerySerializer
from .serializers import PhotoSerializer, PhotoDetailSerializer
from .serializers import EventGenreSerializer, EventGenreDetailSerializer


class EventList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = EventSerializer
    queryset = Event.objects.annotate(
        comments_count=Count('comment', distinct=True),
        interested_count=Count('interesteds', distinct=True),
        goings_count=Count('goings', distinct=True)
    ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    search_fields = [
        'owner__username',
        'title',
        'date'
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'interesteds__owner__profile',
        'goings__owner__profile',
        'owner__profile'
    ]
    orderin_fields = [
        'comments_count',
        'interested_count',
        'goings_count'
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = EventSerializer
    queryset = Event.objects.annotate(
        comments_count=Count('comment', distinct=True),
        interested_count=Count('interesteds', distinct=True),
        goings_count=Count('goings', distinct=True)
    ).order_by('-created_at')


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
    serializer_class = PhotoDetailSerializer
    queryset = Photo.objects.all()


class EventGenreList(generics.ListCreateAPIView):
    serializer_class = EventGenreSerializer
    queryset = EventGenre.objects.all()

    def perform_create(self, serializer):
        if (self.request.user != serializer.validated_data['event'].owner):
            raise ValidationError(
                "You cannot add a genre to somone else event")
        if serializer.validated_data[
         'event'].category != serializer.validated_data['genre'].category:
            raise ValidationError(
                "You can't add a genre of a different event's category"
            )
        serializer.save()


class EventGenreDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsEventOwnerOrReadOnly]
    serializer_class = EventGenreDetailSerializer
    queryset = EventGenre.objects.all()
