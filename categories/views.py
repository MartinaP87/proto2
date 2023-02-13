from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from drf_api_event.permissions import IsAdminOrReadOnly
from .models import Category, Genre
from .serializers import CategorySerializer, GenreSerializer


class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class GenreList(generics.ListAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class CategoryDetail(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Genre.objects.all()


class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    # def get_object(self, pk):
    #     try:
    #         category = Category.objects.get(pk=pk)
    #         return category
    #     except Category.DoesNotExist:
    #         raise Http404

    # def get(self, request, pk):
    #     category = self.get_object(pk)
    #     serializer = CategorySerializer(category)
    #     return Response(serializer.data)

    # def put(self, request, pk):
    #     category = self.get_object(pk)
    #     serializer = CategorySerializer(category, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

