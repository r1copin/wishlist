from rest_framework import generics, permissions
from .models import Wish
from .serializers import WishSerializer


class WishListCreateView(generics.ListCreateAPIView):
    serializer_class = WishSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wish.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WishDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WishSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wish.objects.filter(user=self.request.user)
