from django.urls import path

from .views import ResendCodeView, UserCreateView, VerifyView

urlpatterns = [
    path("user/", UserCreateView.as_view(), name="user_register"),
    path("verify-email/", VerifyView.as_view(), name="auth_verify"),
    path("resend-code/", ResendCodeView.as_view(), name="auth_resend"),
]
