from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions

from account.bl.exceptions import ProfileAlreadyExists, ProfileNotFound
from account.models.profiles import PlayerProfile

from .serializers import PlayerProfileSerializer


class PlayerProfileCreateView(generics.CreateAPIView):
    serializer_class = PlayerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if PlayerProfile.objects.filter(user=self.request.user).exists():
            raise ProfileAlreadyExists()
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Создать профиль игрока",
        description="Создаёт профиль для текущего пользователя.",
        tags=["profiles"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PlayerProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = PlayerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "user_uuid"
    http_method_names = ["get", "patch"]

    @extend_schema(
        summary="Получить профиль игрока",
        description="Возвращает полный профиль игрока по UUID пользователя.",
        tags=["profiles"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Обновить профиль (частичное)",
        description="Частичное обновление профиля игрока. Можно передать только изменяемые поля.",
        tags=["profiles"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def get_object(self):
        user_uuid = self.kwargs["user_uuid"]
        try:
            return PlayerProfile.objects.select_related("user").get(user__pk=user_uuid)
        except PlayerProfile.DoesNotExist:
            raise ProfileNotFound()
