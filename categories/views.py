from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, permissions
from drf_api_event.permissions import IsAdminOrReadOnly
from .models import Category, Genre
from .serializers import CategorySerializer, GenreSerializer


class CategoryList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            return serializer.save()


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class GenreList(generics.ListAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
