from django.urls import path
from .views import RegistrationApiView,LoginApiView,TestApiView

urlpatterns = [
    path('register/',RegistrationApiView.as_view()),
    path('login/',LoginApiView.as_view()),
    path('test/',TestApiView.as_view())
]