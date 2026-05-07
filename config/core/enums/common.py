from django.db import models


class RatingType(models.IntegerChoices):
    classic = 1, "Классический"
    elo = 2, "ELO"


class Priority(models.IntegerChoices):
    low = 1, "Низкий"
    medium = 2, "Средний"
    high = 3, "Высокий"
    critical = 4, "Критический"
