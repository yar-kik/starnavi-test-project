from django.urls import path

from .views import HelloWorld

app_name = "analytics"
urlpatterns = [
    path("", HelloWorld.as_view()),
]
