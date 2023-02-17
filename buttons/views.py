from rest_framework import generics, permissions
from drf_api_event.permissions import IsOwnerOrReadOnly
from .models import Interested, Going, Like
from .serializers import InterestedSerializer, GoingSerializer, LikeSerializer


class InterestedList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = InterestedSerializer
    queryset = Interested.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class InterestedDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = InterestedSerializer
    queryset = Interested.objects.all()


class GoingList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = GoingSerializer
    queryset = Going.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GoingDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = GoingSerializer
    queryset = Going.objects.all()


class LikeList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
