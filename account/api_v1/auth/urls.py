from django.urls import path

from .views import LoginView, LogoutView, RefreshView

urlpatterns = [
    path("login/", LoginView.as_view(), name="auth_login"),
    path("refresh/", RefreshView.as_view(), name="auth_refresh"),
    path("logout/", LogoutView.as_view(), name="auth_logout"),
]
