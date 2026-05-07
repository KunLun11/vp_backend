from django.db import models

from config.core.enums.notifications import NotificationCategory, NotificationType
from etc.models.bases import UUIDTimeBaseModel


class Notification(UUIDTimeBaseModel):
    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    user = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="Пользователь",
    )
    type = models.PositiveSmallIntegerField(
        "Тип уведомления",
        choices=NotificationType.choices,
    )
    category = models.PositiveSmallIntegerField(
        "Категория уведомления",
        choices=NotificationCategory.choices,
    )
    title = models.CharField("Заголовок", max_length=200)
    message = models.TextField("Текст")
    is_read = models.BooleanField("Прочитано", default=False, db_index=True)
    sent_at = models.DateTimeField("Отправлено в", null=True, blank=True)

    def __str__(self):
        return f"{self.title} -> {self.user.email}"
