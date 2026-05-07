from django.db import models


class UserRole(models.TextChoices):
    player = "player", "Игрок"
    coach = "coach", "Тренер"
    organizer = "organizer", "Организатор"
    admin = "admin", "Админ"


class Gender(models.TextChoices):
    male = "M", "Мужской"
    female = "F", "Женский"


class SkillLevel(models.IntegerChoices):
    low = 1, "Начальный"
    low_plus = 2, "Начальный +"
    avg_minus = 3, "Средний -"
    avg = 4, "Средний"
    avg_plus = 5, "Средний +"
    high_minus = 6, "Высокий -"
    high = 7, "Высокий"
    high_plus = 8, "Высокий +"
    pro = 9, "Профи"


class PlayerPosition(models.IntegerChoices):
    opposite = 1, "Диагональный"
    setter = 2, "Связующий"
    middle_blokker = 3, "Центральный блокирующий"
    spiker = 4, "Доигровщик"
    universal = 5, "Универсал"
    libero = 6, "Либеро"


