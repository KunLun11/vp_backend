from django.db import transaction

from account.models.profiles import OrganizerProfile
from config.core.enums.games import GameStatus
from etc.models.location import Location
from game.bl.exceptions import GameNotFound, NotAnOrganizer
from game.filters import GameFilter
from game.models import Game


class GameOrganizerService:
    @staticmethod
    def _get_organizer(user):
        try:
            return OrganizerProfile.objects.get(user=user)
        except OrganizerProfile.DoesNotExist:
            raise NotAnOrganizer()

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
    def get_organized_games(cls, user, filters: dict = None):
        organizer = cls._get_organizer(user)
        games = Game.objects.filter(organizer=organizer).select_related("location")
        if filters:
            game_filter = GameFilter(filters, queryset=games)
            if game_filter.is_valid():
                games = game_filter.qs
            else:
                games = Game.objects.none()
        return games.order_by("-date_time")

    @classmethod
    @transaction.atomic
    def create_game(cls, user, data: dict) -> Game:
        organizer = cls._get_organizer(user)
        try:
            location = Location.objects.get(pk=data.pop("location_id"))
        except Location.DoesNotExist:
            raise ValueError(
                "Указанная локация не найдена"
            )
        status = data.pop("status", None) or GameStatus.draft
        game = Game.objects.create(organizer=organizer, location=location, status=status, **data)
        return game

    @classmethod
    @transaction.atomic
    def publish_game(cls, user, game_id: int) -> Game:
        organizer = cls._get_organizer(user)
        game = cls._get_game(game_id, select_for_update=True)
        if game.organizer != organizer:
            raise NotAnOrganizer(detail="Вы не организатор этой игры")
        if game.status != GameStatus.draft:
            raise ValueError("Игра не является черновиком")
        game.status = GameStatus.registration_open
        game.save(update_fields=["status"])
        return game

    @classmethod
    @transaction.atomic
    def close_registration(cls, user, game_id: int) -> Game:
        organizer = cls._get_organizer(user)
        game = cls._get_game(game_id, select_for_update=True)
        if game.organizer != organizer:
            raise NotAnOrganizer()
        if game.status != GameStatus.registration_open:
            raise ValueError("Закрыть запись можно только для открытой игры")
        game.status = GameStatus.registration_closed
        game.save(update_fields=["status"])
        return game

    @classmethod
    @transaction.atomic
    def complete_game(cls, user, game_id: int) -> Game:
        organizer = cls._get_organizer(user)
        game = cls._get_game(game_id, select_for_update=True)
        if game.organizer != organizer:
            raise NotAnOrganizer()
        if game.status not in (GameStatus.in_progress,):
            raise ValueError("Завершить можно только идущую игру")
        game.status = GameStatus.completed
        game.save(update_fields=["status"])
        return game

    @classmethod
    @transaction.atomic
    def cancel_game(cls, user, game_id: int) -> Game:
        organizer = cls._get_organizer(user)
        game = cls._get_game(game_id, select_for_update=True)
        if game.organizer != organizer:
            raise NotAnOrganizer()
        if game.status in (GameStatus.cancelled, GameStatus.completed):
            raise ValueError("Игра уже отменена или завершена")
        game.status = GameStatus.cancelled
        game.save(update_fields=["status"])
        return game
