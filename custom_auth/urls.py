from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.RegisterAPIView.as_view()),
    path("code-verification/", views.CodeVerificationAPIView.as_view()),

]