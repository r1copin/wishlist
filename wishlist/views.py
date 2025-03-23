from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
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


class ReserveWishView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        wish = get_object_or_404(Wish, pk=pk)

        if wish.user == request.user:
            return Response({"error": "You can't reserve your own wish."}, status=status.HTTP_403_FORBIDDEN)

        if wish.gift_by and wish.gift_by != request.user:
            return Response({"error": "This wish is already reserved."}, status=status.HTTP_409_CONFLICT)

        wish.gift_by = request.user
        wish.save()

        return Response({"error": "Wish reserved successfully."}, status=status.HTTP_200_OK)


class UnreserveWishView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        wish = get_object_or_404(Wish, pk=pk)

        if request.user != wish.gift_by and request.user != wish.user:
            return Response({"error": "You can't unreserve this wish."}, status=status.HTTP_403_FORBIDDEN)

        if not wish.gift_by:
            return Response({"error": "This wish is not reserved."}, status=status.HTTP_400_BAD_REQUEST)

        wish.gift_by = None
        wish.save()

        return Response({"error": "Wish unreserved successfully."}, status=status.HTTP_200_OK)
