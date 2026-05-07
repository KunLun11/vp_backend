from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from account.models.profiles import OrganizerProfile
from game.api_v1.base import GameBaseViewSet
from game.api_v1.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from game.api_v1.serializers import (
    AttendSerializer,
    CancelGameSerializer,
    CancelRegistrationSerializer,
    CloseRegistrationSerializer,
    CompleteGameSerializer,
    ConfirmParticipantSerializer,
    CreateGameSerializer,
    GameDetailSerializer,
    GameListSerializer,
    GameParticipantSerializer,
    NoShowSerializer,
    PublishGameSerializer,
    RegisterOnGameSerializer,
)
from game.filters import GameFilter
from game.models import Game, GameParticipant


@extend_schema_view(
    list=extend_schema(
        summary="Список игр",
        description="Публичный список игр с фильтрацией и пагинацией.",
        auth=None,
        tags=["games"],
    ),
    retrieve=extend_schema(
        summary="Детали игры",
        description="Полная информация об игре.",
        auth=None,
        tags=["games"],
    ),
    create=extend_schema(
        summary="Создать игру",
        description="Создаёт игру в статусе «Черновик».",
        tags=["games"],
    ),
)
class GameViewSet(
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    GameBaseViewSet,
):
    filterset_class = GameFilter

    serializer_action_map = {
        "list": GameListSerializer,
        "retrieve": GameDetailSerializer,
        "create": CreateGameSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_action_map.get(self.action, GameDetailSerializer)

    def list(self, request, *args, **kwargs):
        return self.list_endpoint(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return self.create_endpoint(request, response_serializer_class=GameDetailSerializer)

    def retrieve(self, request, *args, **kwargs):
        return self.retrieve_endpoint(request, *args, **kwargs)

    def _execute_action(self, serializer_class, status_code=status.HTTP_200_OK, output_serializer=None):
        context = {
            "request": self.request,
            "game_id": int(self.kwargs["pk"]),
            **self.kwargs,
        }
        ser = serializer_class(data=self.request.data or {}, context=context)
        ser.is_valid(raise_exception=True)
        result = ser.save()
        if result is None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        if output_serializer:
            return Response(output_serializer(result).data, status=status_code)
        return Response(status=status_code)

    @extend_schema(
        summary="Опубликовать игру",
        tags=["games"],
    )
    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        return self._execute_action(PublishGameSerializer, output_serializer=GameDetailSerializer)

    @extend_schema(
        summary="Закрыть запись",
        tags=["games"],
    )
    @action(detail=True, methods=["post"], url_path="close-registration")
    def close_registration(self, request, pk=None):
        return self._execute_action(CloseRegistrationSerializer, output_serializer=GameDetailSerializer)

    @extend_schema(
        summary="Завершить игру",
        tags=["games"],
    )
    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        return self._execute_action(CompleteGameSerializer, output_serializer=GameDetailSerializer)

    @extend_schema(
        summary="Отменить игру",
        tags=["games"],
    )
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        return self._execute_action(CancelGameSerializer, output_serializer=GameDetailSerializer)

    @extend_schema(
        summary="Записаться на игру",
        tags=["games"],
    )
    @action(detail=True, methods=["post"], url_path="register")
    def register_player(self, request, pk=None):
        return self._execute_action(
            RegisterOnGameSerializer, status_code=status.HTTP_201_CREATED, output_serializer=GameParticipantSerializer
        )

    @extend_schema(
        summary="Отменить запись",
        tags=["games"],
    )
    @action(detail=True, methods=["post"], url_path="cancel-registration")
    def cancel_registration(self, request, pk=None):
        return self._execute_action(CancelRegistrationSerializer, status_code=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Подтвердить участие",
        tags=["games"],
    )
    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):
        return self._execute_action(ConfirmParticipantSerializer, output_serializer=GameParticipantSerializer)

    @extend_schema(
        summary="Отметиться присутствовавшим",
        tags=["games"],
    )
    @action(detail=True, methods=["post"])
    def attend(self, request, pk=None):
        return self._execute_action(AttendSerializer, output_serializer=GameParticipantSerializer)

    @extend_schema(
        summary="Отметить неявку",
        tags=["games"],
    )
    @action(detail=True, methods=["post"], url_path=r"no-show/(?P<participant_id>\d+)")
    def no_show(self, request, pk=None, participant_id=None):
        context = {
            "request": self.request,
            "game_id": int(pk),
            "participant_id": int(participant_id),
        }
        ser = NoShowSerializer(data={"participant_id": int(participant_id)}, context=context)
        ser.is_valid(raise_exception=True)
        participant = ser.save()
        return Response(GameParticipantSerializer(participant).data)

    @extend_schema(
        summary="Мои игры",
        tags=["games"],
    )
    @action(detail=False, methods=["get"], url_path="my-games")
    def my_games(self, request):
        participants = (
            GameParticipant.objects.select_related("game__location")
            .filter(player__user=request.user)
            .order_by("-registered_at")
        )
        data = [
            {
                "game": GameListSerializer(participant.game).data,
                "status": participant.status,
                "participant_id": participant.id,
            }
            for participant in participants
        ]
        return Response(data)

    @extend_schema(
        summary="Мои организованные игры",
        tags=["games"],
    )
    @action(detail=False, methods=["get"], url_path="organized")
    def organized_games(self, request):
        try:
            organizer = OrganizerProfile.objects.get(user=request.user)
        except OrganizerProfile.DoesNotExist:
            return Response({"detail": "Вы не организатор"}, status=status.HTTP_403_FORBIDDEN)
        games = Game.objects.filter(organizer=organizer).select_related("location").order_by("-date_time")
        filterset = GameFilter(request.query_params, queryset=games)
        serializer = GameListSerializer(filterset.qs, many=True)
        return Response(serializer.data)
