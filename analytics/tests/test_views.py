from rest_framework.test import APITestCase

from authentication.models import User


class TestLikeApiView(APITestCase):
    def test_post_analytics(self):
        response = self.client.get("/api/analytics/posts/")
        self.assertEqual(response.status_code, 200)


class TestUserActivityApiView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user", email="email@mail.com", password="password"
        )

    def test_user_activity(self):
        response = self.client.get("/api/analytics/users/1/")
        self.assertEqual(response.status_code, 200)
