from django.db import models

from config.core.enums.games import GameStatus, GenderRestriction, ParticipantStatus
from config.core.enums.users import SkillLevel
from etc.models.bases import IDTimeBaseModel


class Game(IDTimeBaseModel):
    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"
        indexes = [
            models.Index(fields=["status", "date_time"]),
        ]

    organizer = models.ForeignKey(
        "account.OrganizerProfile",
        on_delete=models.CASCADE,
        related_name="games",
        verbose_name="Организатор",
    )
    location = models.ForeignKey(
        "etc.Location",
        on_delete=models.PROTECT,
        related_name="games",
        verbose_name="Место проведения",
    )
    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", blank=True)
    date_time = models.DateTimeField("Дата и время")
    duration_minutes = models.IntegerField("Длительность (мин)")
    capacity = models.IntegerField("Вместимость", default=12)
    booked_count = models.IntegerField("Записано", default=0)
    min_players = models.IntegerField("Минимум игроков", default=10)
    cancel_reason = models.CharField("Причина отмены", max_length=100, blank=True)
    cancelled_at = models.DateTimeField("Отменена в", null=True, blank=True)
    price = models.DecimalField(
        "Цена",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    skill_level = models.PositiveSmallIntegerField(
        "Требуемый уровень",
        choices=SkillLevel.choices,
        default=SkillLevel.avg,
    )
    gender = models.PositiveSmallIntegerField(
        "Пол",
        choices=GenderRestriction.choices,
        default=GenderRestriction.unrestricted,
    )
    status = models.PositiveSmallIntegerField(
        "Статус",
        choices=GameStatus.choices,
        default=GameStatus.draft,
    )
    elo_rating_change = models.IntegerField(
        "Изменение ELO",
        null=True,
        blank=True,
    )
    is_tournament = models.BooleanField("Турнирная игра", default=False)

    def __str__(self):
        return f"{self.title} ({self.date_time})"

    def get_available_slots(self):
        return self.capacity - self.booked_count


class GameParticipant(IDTimeBaseModel):
    class Meta:
        verbose_name = "Участник игры"
        verbose_name_plural = "Участники игр"
        unique_together = ["game", "player"]

    game = models.ForeignKey(
        "game.Game",
        on_delete=models.CASCADE,
        related_name="game_participants",
        verbose_name="Игра",
    )
    player = models.ForeignKey(
        "account.PlayerProfile",
        on_delete=models.CASCADE,
        related_name="game_participants",
        verbose_name="Игрок",
    )
    status = models.PositiveSmallIntegerField(
        "Статус",
        choices=ParticipantStatus.choices,
        default=ParticipantStatus.registered,
    )
    registered_at = models.DateTimeField("Дата записи", auto_now_add=True)
    cancelled_at = models.DateTimeField("Дата отмены", null=True, blank=True)
    checked_in_at = models.DateTimeField("Дата отметки", null=True, blank=True)
    elo_before = models.IntegerField("ELO до", null=True, blank=True)
    elo_after = models.IntegerField("ELO после", null=True, blank=True)
    is_paid_marked = models.BooleanField("Оплата подтверждена организатором", default=False)
    paid_comment = models.CharField("Комментарий к оплате", max_length=255, blank=True)
    paid_marked_at = models.DateTimeField("Оплата подтверждена в", null=True, blank=True)

    def __str__(self):
        return f"{self.player} -> {self.game.title}"


class GameReview(IDTimeBaseModel):
    class Meta:
        verbose_name = "Отзыв об игре"
        verbose_name_plural = "Отзывы об играх"
        unique_together = ["game", "player"]

    game = models.ForeignKey(
        "game.Game",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Игра",
    )
    player = models.ForeignKey(
        "account.PlayerProfile",
        on_delete=models.CASCADE,
        related_name="game_reviews",
        verbose_name="Игрок",
    )
    rating_game = models.IntegerField("Рейтинг игры", default=5)
    comment = models.TextField("Комментарии", null=True, blank=True)

    def __str__(self):
        return f"Отзыв на {self.game.title} от {self.player}"
