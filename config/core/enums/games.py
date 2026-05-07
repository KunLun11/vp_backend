from django.db import models


class GameStatus(models.IntegerChoices):
    draft = 0, "Черновик"
    registration_open = 1, "Запись открыта"
    registration_closed = 2, "Запись окончена"
    in_progress = 3, "Идёт"
    completed = 4, "Завершено"
    cancelled = 5, "Отменено"


class ParticipantStatus(models.IntegerChoices):
    registered = 1, "Записан"
    confirmed = 2, "Подтверждён"
    attended = 3, "Присутствовал"
    no_show = 4, "Не пришел"


class GenderRestriction(models.IntegerChoices):
    unrestricted = 0, "Без ограничений"
    male_only = 1, "Только мужчины"
    female_only = 2, "Только женщины"
    mixed = 3, "Смешанная"
