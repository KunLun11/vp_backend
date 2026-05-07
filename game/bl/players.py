from uuid import UUID

from django.db import transaction
from django.utils import timezone

from account.models.profiles import PlayerProfile
from chat.bl.chat_service import ChatService
from config.core.enums.games import GameStatus, ParticipantStatus
from game.bl.exceptions import (
    AlreadyRegistered,
    GameFull,
    GameNotFound,
    GameRegistrationClosed,
    NotAnOrganizer,
    NotAPlayer,
    RegistrationNotFound,
)
from game.filters import GameFilter
from game.models import Game, GameParticipant


class GamePlayerService:
    @staticmethod
    def _get_player(user_uuid: UUID) -> PlayerProfile:
        try:
            return PlayerProfile.objects.select_related("user").get(user__pk=user_uuid)
        except PlayerProfile.DoesNotExist:
            raise NotAPlayer()

    @staticmethod
    def _get_game(game_id: int, select_for_update: bool = False) -> Game:
        qs = Game.objects.all()
        if select_for_update:
            qs = qs.select_for_update()
        try:
            return qs.get(pk=game_id)
        except Game.DoesNotExist:
            raise GameNotFound()

    @classmethod
    def get_games_list(cls, filters: dict):
        games = Game.objects.select_related("location").all()
        game_filter = GameFilter(filters, queryset=games)
        if not game_filter.is_valid():
            return Game.objects.none()
        games = game_filter.qs.order_by("date_time")
        offset = int(filters.get("offset", 0))
        limit = int(filters.get("limit", 20))
        return games[offset : offset + limit]

    @classmethod
    def get_my_games(cls, user_uuid: UUID):
        participants = (
            GameParticipant.objects.select_related("game__location")
            .filter(player__user__pk=user_uuid)
            .order_by("-registered_at")
        )
        return participants

    @classmethod
    @transaction.atomic
    def register_player(cls, user_uuid: UUID, game_id: int) -> GameParticipant:
        player = cls._get_player(user_uuid)
        game = cls._get_game(game_id, select_for_update=True)
        if game.status != GameStatus.registration_open:
            raise GameRegistrationClosed()
        if game.get_available_slots() <= 0:
            raise GameFull()
        if GameParticipant.objects.filter(game=game, player=player).exists():
            raise AlreadyRegistered()
        participant = GameParticipant.objects.create(
            game=game,
            player=player,
            status=ParticipantStatus.registered,
        )
        ChatService.add_participant_to_chat(participant)
        game.booked_count += 1
        if game.booked_count >= game.capacity:
            game.status = GameStatus.registration_closed
        game.save(update_fields=["booked_count", "status"])
        return participant

    @classmethod
    @transaction.atomic
    def cancel_registration(cls, user_uuid: UUID, game_id: int):
        player = cls._get_player(user_uuid)
        game = cls._get_game(game_id, select_for_update=True)
        try:
            participant = GameParticipant.objects.get(game=game, player=player, status=ParticipantStatus.registered)
        except GameParticipant.DoesNotExist:
            raise RegistrationNotFound()
        participant.status = ParticipantStatus.cancelled
        participant.cancelled_at = timezone.now()
        participant.save(update_fields=["status", "cancelled_at"])
        game.booked_count -= 1
        game.save(update_fields=["booked_count"])

    @classmethod
    @transaction.atomic
    def confirm_participant(cls, user_uuid: UUID, game_id: int) -> GameParticipant:
        player = cls._get_player(user_uuid)
        try:
            participant = GameParticipant.objects.get(
                game_id=game_id, player=player, status=ParticipantStatus.registered
            )
        except GameParticipant.DoesNotExist:
            raise RegistrationNotFound(detail="Вы не записаны или уже подтверждены")
        participant.status = ParticipantStatus.confirmed
        participant.save(update_fields=["status"])
        return participant

    @classmethod
    @transaction.atomic
    def mark_attended(cls, user_uuid: UUID, game_id: int) -> GameParticipant:
        player = cls._get_player(user_uuid)
        game = cls._get_game(game_id)
        if game.status != GameStatus.in_progress:
            raise ValueError("Отметка присутствия доступна только во время игры")
        try:
            participant = GameParticipant.objects.get(
                game_id=game_id, player=player, status=ParticipantStatus.confirmed
            )
        except GameParticipant.DoesNotExist:
            raise RegistrationNotFound(detail="Вы не подтверждены на игру")
        participant.status = ParticipantStatus.attended
        participant.checked_in_at = timezone.now()
        participant.save(update_fields=["status", "checked_in_at"])
        return participant

    @classmethod
    @transaction.atomic
    def mark_no_show(cls, user, game_id: int, participant_id: int) -> GameParticipant:
        from account.models.profiles import OrganizerProfile

        try:
            organizer = OrganizerProfile.objects.get(user=user)
        except OrganizerProfile.DoesNotExist:
            raise NotAnOrganizer()
        game = cls._get_game(game_id)
        if game.organizer != organizer:
            raise NotAnOrganizer(detail="Вы не организатор этой игры")
        try:
            participant = GameParticipant.objects.get(id=participant_id, game_id=game_id)
        except GameParticipant.DoesNotExist:
            raise RegistrationNotFound(detail="Участник не найден")
        if participant.status not in (ParticipantStatus.confirmed, ParticipantStatus.attended):
            raise ValueError("Нельзя отметить как не пришедшего")
        participant.status = ParticipantStatus.no_show
        participant.save(update_fields=["status"])
        return participant
