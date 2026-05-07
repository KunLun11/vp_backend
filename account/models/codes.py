from django.db import models

from etc.models.bases import IDTimeBaseModel


class EmailConfirmationCode(IDTimeBaseModel):
    class Meta:
        verbose_name = "Код подтверждения"
        verbose_name_plural = "Коды подтверждения"
    
    user = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="codes",
        verbose_name="Пользователь",
    )
    code_hash = models.CharField("Код", max_length=64, db_index=True)
    expires_at = models.DateTimeField("Время истечения")
    is_used = models.BooleanField("Использован", default=False)


