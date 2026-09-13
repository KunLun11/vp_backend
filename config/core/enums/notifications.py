from django.db import models


class NotificationType(models.IntegerChoices):
    email = 1, "email"
    push = 2, "push"
    telegram = 4, "telegram"


class NotificationCategory(models.IntegerChoices):
    registration = 1, "Регистрация"
    booking_confirmation = 2, "Подтверждение записи"
    reminder = 3, "Напоминание"
    cancellation = 4, "Отмена"
    review_request = 5, "Запрос отзыва"
    tournament_invite = 6, "Приглашение на турнир"
