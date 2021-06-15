from django.urls import path

from .views import BookStatisticsApiView, UserActivityApiView

app_name = "analytics"
urlpatterns = [
    path("posts/", BookStatisticsApiView.as_view()),
    path("users/<int:user_id>/", UserActivityApiView.as_view()),
]
