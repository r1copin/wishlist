from django.urls import path
from .views import (
    WishListCreateView,
    WishDetailView,
    ReserveWishView,
    UnreserveWishView,
)


urlpatterns = [
    path("wishes/", WishListCreateView.as_view(), name="wish-list-create"),
    path("wishes/<int:pk>/", WishDetailView.as_view(), name="wish-detail"),
    path("wishes/<int:pk>/reserve/", ReserveWishView.as_view(), name="wish-reserve"),
    path(
        "wishes/<int:pk>/unreserve/", UnreserveWishView.as_view(), name="wish-unreserve"
    ),
]
