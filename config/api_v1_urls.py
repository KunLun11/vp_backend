from django.urls import include, path

urlpatterns = [
    path("auth/", include("account.api_v1.auth.urls")),
    path("register/", include("account.api_v1.registration.urls")),
    path("profiles/", include("account.api_v1.profiles.urls")),
    path("users/", include("account.api_v1.users.urls")),
    path("chats/", include("chat.api_v1.urls")),
    path("", include("game.api_v1.urls")),
]
