from django.db import models

from config.core.enums.common import RatingReason, RatingType
from etc.models.bases import IDTimeBaseModel


class RatingHistory(IDTimeBaseModel):
    class Meta:
        verbose_name = "История рейтинга"
        verbose_name_plural = "История рейтингов"
        indexes = [
            models.Index(fields=["user", "rating_type", "-created_at"]),
        ]

    user = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="rating_history",
    )
    game = models.ForeignKey(
        "game.Game",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rating_changes",
    )
    rating_type = models.PositiveSmallIntegerField(
        "Тип рейтинга",
        choices=RatingType.choices,
        default=RatingType.elo,
    )
    delta = models.IntegerField("Изменение")
    reason = models.PositiveSmallIntegerField(
        "Причина",
        choices=RatingReason.choices,
    )
    comment = models.CharField("Комментарий", max_length=255, blank=True)


class GameAgreement(IDTimeBaseModel):
    class Meta:
        verbose_name = "Соглашение с судейством"
        verbose_name_plural = "Соглашения с судейством"
        unique_together = ["game", "user"]

    game = models.ForeignKey("game.Game", on_delete=models.CASCADE, related_name="agreements")
    user = models.ForeignKey("account.User", on_delete=models.CASCADE, related_name="agreements")
    accepted_at = models.DateTimeField("Принято", auto_now_add=True)
