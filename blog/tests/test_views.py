from rest_framework.response import Response
from rest_framework.test import APITestCase

from authentication.models import User
from blog.models import Post


class TestListPostApiView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user", email="email@mail.com", password="password"
        )

    def test_create_post_if_unauthorized(self):
        response = self.client.post("/api/blog/posts/")
        self.assertEqual(response.status_code, 403)

    def test_create_post_if_empty_input(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.post("/api/blog/posts/")
        self.assertEqual(response.status_code, 400)

    def test_create_post_if_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.post(
            "/api/blog/posts/", data={"post": {"title": ""}}
        )
        self.assertEqual(response.status_code, 400)

    def test_create_post_successfully(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.post(
            "/api/blog/posts/",
            data={"post": {"title": "Post title", "body": "Post body"}},
        )
        self.assertEqual(response.status_code, 201)
        post = Post.objects.first()
        self.assertEqual(post.title, "Post title")

    def test_get_posts_list(self):
        Post.objects.create(
            title="Post title", body="Post body", author=self.user
        )
        response: Response = self.client.get("/api/blog/posts/")
        self.assertEqual(response.status_code, 200)
        posts = response.json()["posts"]
        self.assertEqual(posts[0]["title"], "Post title")


class TestPostApiView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user", email="email@mail.com", password="password"
        )
        cls.user2 = User.objects.create_user(
            username="user2", email="email2@mail.com", password="password"
        )

    def test_get_post_if_not_exist(self):
        response = self.client.get("/api/blog/posts/1/")
        self.assertEqual(response.status_code, 404)

    def test_get_post_successfully(self):
        Post.objects.create(
            title="Post title", body="Post body", author=self.user
        )
        response = self.client.get("/api/blog/posts/1/")
        self.assertEqual(response.status_code, 200)

    def test_update_post_if_not_authorized(self):
        response = self.client.patch("/api/blog/posts/1/")
        self.assertEqual(response.status_code, 403)

    def test_update_post_if_not_exists(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.patch("/api/blog/posts/1/")
        self.assertEqual(response.status_code, 404)

    def test_update_post_if_not_author(self):
        Post.objects.create(
            title="Post title", body="Post body", author=self.user2
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.patch("/api/blog/posts/1/")
        self.assertEqual(response.status_code, 403)

    def test_update_post_if_empty_request(self):
        Post.objects.create(
            title="Post title", body="Post body", author=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.patch("/api/blog/posts/1/")
        self.assertEqual(response.status_code, 400)

    def test_update_post_successfully(self):
        Post.objects.create(
            title="Post title", body="Post body", author=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.patch(
            "/api/blog/posts/1/", data={"post": {"title": "Updated title"}}
        )
        self.assertEqual(response.status_code, 200)
        post = Post.objects.first()
        self.assertEqual(post.title, "Updated title")

    def test_delete_post_if_not_exists(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.delete("/api/blog/posts/1/")
        self.assertEqual(response.status_code, 404)

    def test_delete_post_if_not_authorized(self):
        Post.objects.create(
            title="Post title", body="Post body", author=self.user
        )
        response = self.client.delete("/api/blog/posts/1/")
        self.assertEqual(response.status_code, 403)

    def test_delete_post_if_not_author(self):
        Post.objects.create(
            title="Post title", body="Post body", author=self.user2
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.delete("/api/blog/posts/1/")
        self.assertEqual(response.status_code, 403)

    def test_delete_post_successfully(self):
        Post.objects.create(
            title="Post title", body="Post body", author=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.delete("/api/blog/posts/1/")
        self.assertEqual(response.status_code, 200)
        post = Post.objects.all()
        self.assertEqual(post.count(), 0)


class TestLikeApiView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user", email="email@mail.com", password="password"
        )
        cls.post = Post.objects.create(
            title="Post title", body="Post body", author=cls.user
        )

    def test_like_if_not_authorized(self):
        response = self.client.get("/api/blog/posts/1/like/")
        self.assertEqual(response.status_code, 403)

    def test_like_if_post_not_exists(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.get("/api/blog/posts/2/like/")
        self.assertEqual(response.status_code, 404)

    def test_like_if_post_not_liked_yet(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        response = self.client.get("/api/blog/posts/1/like/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["detail"], "Post was liked")

    def test_like_if_post_was_liked(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user.token)
        self.client.get("/api/blog/posts/1/like/")
        response = self.client.get("/api/blog/posts/1/like/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["detail"], "Post was unliked")
