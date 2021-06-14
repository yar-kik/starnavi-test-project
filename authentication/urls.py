from django.urls import path
from .views import RegistrationApiView

app_name = 'authentication'
urlpatterns = [
    path('registration/', RegistrationApiView.as_view()),
]
