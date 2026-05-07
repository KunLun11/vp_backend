from django.db import models

from config.core.enums.users import PlayerPosition, SkillLevel
from etc.models.base_profiles import BaseProfile


class PlayerProfile(BaseProfile):
    class Meta:
        verbose_name = "Профиль игрока"
        verbose_name_plural = "Профили игроков"
        indexes = [
            models.Index(fields=["skill_level"]),
            models.Index(fields=["elo_rating"]),
        ]

    user = models.OneToOneField(
        "account.User",
        on_delete=models.CASCADE,
        related_name="player_profile",
        verbose_name="Пользователь",
    )
    skill_level = models.PositiveSmallIntegerField(
        "Уровень навыков",
        choices=SkillLevel.choices,
        default=SkillLevel.avg,
    )
    position = models.PositiveSmallIntegerField(
        "Позиция",
        choices=PlayerPosition.choices,
        default=PlayerPosition.universal,
    )
    completion_percentage = models.IntegerField("Заполненность профиля", default=0)
    total_games = models.IntegerField("Игр сыграно", default=0)
    total_tournament = models.IntegerField("Игр на турнире сыграно", default=0)


class CoachProfile(BaseProfile):
    class Meta:
        verbose_name = "Профиль тренера"
        verbose_name_plural = "Профили тренеров"

    user = models.OneToOneField(
        "account.User",
        on_delete=models.CASCADE,
        related_name="coach_profile",
        verbose_name="Тренер",
    )
    experience_years = models.IntegerField("Опыт(лет)")
    certifications = models.TextField("Сертификаты", null=True, blank=True)
    hourly_rate = models.DecimalField(
        "Ставка в час",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    total_traings = models.IntegerField("Проведено игр", default=0)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name} ({self.experience_years} лет опыта)"


class OrganizerProfile(BaseProfile):
    class Meta:
        verbose_name = "Профиль организатора"
        verbose_name = "Профили организаторов"

    user = models.OneToOneField(
        "account.User",
        on_delete=models.CASCADE,
        related_name="organizer_profile",
        verbose_name="Организатор",
    )
    description = models.TextField("Описание", null=True, blank=True)
    total_games = models.IntegerField("Организовано игр", default=0)
