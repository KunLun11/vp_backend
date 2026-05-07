from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from account.bl.auth import JWTAuthentication
from game.models import Game


class GameBaseViewSet(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Game.objects.select_related("organizer", "location").all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = None

    public_actions = ["list", "retrieve"]

    def get_permissions(self):
        if self.action in self.public_actions:
            return []
        return super().get_permissions()

    def get_extra_serializer_context(self):
        return {"request": self.request}
