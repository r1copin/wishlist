from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Wish
from django.contrib.auth import get_user_model

User = get_user_model()


class WishTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tanya-kta", password="123123")
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.auth_header = {"HTTP_AUTHORIZATION": f"Bearer {self.token}"}
        self.wish_data = {
            "title": "Go to Japan",
            "description": "Visit Kyoto and Tokyo during cherry blossom season. And pass PIPO",
        }

    def test_create_wish(self):
        response = self.client.post("/api/wishes/", self.wish_data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wish.objects.count(), 1)
        self.assertEqual(Wish.objects.first().title, "Go to Japan")

    def test_list_wishes(self):
        Wish.objects.create(user=self.user, title="Pass PIPO")
        response = self.client.get("/api/wishes/", **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_wish(self):
        wish = Wish.objects.create(user=self.user, title="Failed PIPO", description="Description")
        update_data = {"title": "Passed PIPO", "description": "Updated description"}
        response = self.client.put(
            f"/api/wishes/{wish.id}/", update_data, **self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        wish.refresh_from_db()
        self.assertEqual(wish.title, "Passed PIPO")

    def test_delete_wish(self):
        wish = Wish.objects.create(user=self.user, title="To delete")
        response = self.client.delete(f"/api/wishes/{wish.id}/", **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Wish.objects.count(), 0)

    def test_unauthenticated_access(self):
        response = self.client.get("/api/wishes/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class WishReservationTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="123123")
        self.reserver = User.objects.create_user(username="reserver", password="456456")
        self.other = User.objects.create_user(username="other", password="789789")

        self.wish = Wish.objects.create(user=self.owner, title="Pass PIPO")

        self.reserve_url = f"/api/wishes/{self.wish.id}/reserve/"
        self.unreserve_url = f"/api/wishes/{self.wish.id}/unreserve/"

    def auth(self, user):
        self.client.force_authenticate(user=user)

    def test_reserve_wish_success(self):
        self.auth(self.reserver)
        response = self.client.post(self.reserve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wish.refresh_from_db()
        self.assertEqual(self.wish.gift_by, self.reserver)

    def test_reserve_already_reserved_wish(self):
        self.wish.gift_by = self.reserver
        self.wish.save()
        self.auth(self.other)
        response = self.client.post(self.reserve_url)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_cannot_reserve_own_wish(self):
        self.auth(self.owner)
        response = self.client.post(self.reserve_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unreserve_by_reserver(self):
        self.wish.gift_by = self.reserver
        self.wish.save()
        self.auth(self.reserver)
        response = self.client.post(self.unreserve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wish.refresh_from_db()
        self.assertIsNone(self.wish.gift_by)

    def test_unreserve_by_owner(self):
        self.wish.gift_by = self.reserver
        self.wish.save()
        self.auth(self.owner)
        response = self.client.post(self.unreserve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wish.refresh_from_db()
        self.assertIsNone(self.wish.gift_by)

    def test_unreserve_by_other_user_denied(self):
        self.wish.gift_by = self.reserver
        self.wish.save()
        self.auth(self.other)
        response = self.client.post(self.unreserve_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unreserve_unreserved_wish(self):
        self.auth(self.owner)
        response = self.client.post(self.unreserve_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
