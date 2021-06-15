from django.urls import path

from .views import LoginApiView, RegistrationApiView, UserActivityApiView

app_name = "authentication"
urlpatterns = [
    path("registration/", RegistrationApiView.as_view()),
    path("login/", LoginApiView.as_view()),
    path("users/<int:user_id>/activity/", UserActivityApiView.as_view()),
]
