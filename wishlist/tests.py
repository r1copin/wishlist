from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Wish
from django.contrib.auth import get_user_model
User = get_user_model()


class WishTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpass123")
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.auth_header = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        self.wish_data = {
            "title": "Go to Japan",
            "description": "Visit Kyoto and Tokyo during cherry blossom season."
        }

    def test_create_wish(self):
        response = self.client.post("/api/wishes/", self.wish_data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wish.objects.count(), 1)
        self.assertEqual(Wish.objects.first().title, "Go to Japan")

    def test_list_wishes(self):
        Wish.objects.create(user=self.user, title="Climb Everest")
        response = self.client.get("/api/wishes/", **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_wish(self):
        wish = Wish.objects.create(user=self.user, title="Old Title", description="...")
        update_data = {"title": "New Title", "description": "Updated desc"}
        response = self.client.put(f"/api/wishes/{wish.id}/", update_data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        wish.refresh_from_db()
        self.assertEqual(wish.title, "New Title")

    def test_delete_wish(self):
        wish = Wish.objects.create(user=self.user, title="Temporary")
        response = self.client.delete(f"/api/wishes/{wish.id}/", **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Wish.objects.count(), 0)

    def test_unauthenticated_access(self):
        response = self.client.get("/api/wishes/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
