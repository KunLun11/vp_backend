from django.db import models


class BlackListedToken(models.Model):
    class Meta:
        verbose_name = "Истекший токен"
        verbose_name_plural = "Истекшие токены" 
        ordering = ("-created_at",)

    jti = models.UUIDField(unique=True, db_index=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="tokens",
        verbose_name="Пользователь",
    )
