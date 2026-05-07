from django.urls import path

from .views import PlayerProfileCreateView, PlayerProfileRetrieveUpdateView

urlpatterns = [
    path("profile/", PlayerProfileCreateView.as_view(), name="profile-create"),
    path("users/<uuid:user_uuid>/profile/", PlayerProfileRetrieveUpdateView.as_view(), name="profile-detail"),
]
