from django.urls import path

from blog.views import ListPostApiView, PostApiView, LikeApiView

app_name = "blog"
urlpatterns = [
    path("posts/", ListPostApiView.as_view()),
    path("posts/<int:post_id>/", PostApiView.as_view()),
    path("posts/<int:post_id>/like/", LikeApiView.as_view()),
]
