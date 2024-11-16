from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.RegisterAPIView.as_view()),
    path("code-verification/", views.CodeVerificationAPIView.as_view()),
    path("login/", views.LoginAPIView.as_view()),
    path("token-test/", views.TestTokenAPIView.as_view()),
    path("logout/", views.LogOutAPIView.as_view()),

]