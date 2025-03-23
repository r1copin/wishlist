from django.urls import path
from .views import WishListCreateView, WishDetailView


urlpatterns = [
    path("wishes/", WishListCreateView.as_view(), name="wish-list-create"),
    path("wishes/<int:pk>/", WishDetailView.as_view(), name="wish-detail"),
]
