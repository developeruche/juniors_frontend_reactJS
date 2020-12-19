from django.urls import path
from .views import LoginView, RegisterView, RefreshView, PreRestPassword, ResetPassword

urlpatterns = [
    path("login", LoginView.as_view()),
    path("register", RegisterView.as_view()),
    path("refresh", RefreshView.as_view()),
    path("pre-password-reset", PreRestPassword.as_view()),
    path("password-reset/<reset_url>", ResetPassword.as_view()),
]
