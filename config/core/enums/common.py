from django.db import models


class RatingType(models.IntegerChoices):
    elo = 2, "ELO"


class RatingReason(models.IntegerChoices):
    game_played = 1, "Сыграна игра"
    win = 2, "Победа"
    loss = 3, "Поражение"
    draw = 4, "Ничья"
    no_show = 5, "Неявка"
    late_cancel = 6, "Поздняя отмена"
    game_cancelled = 7, "Игра отменена организатором"
    game_low_fill = 8, "Недобор игроков"
    game_success = 9, "Успешно проведённая игра"
    manual = 10, "Ручная корректировка"
