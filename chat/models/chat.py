from django.db import models
from django.utils import timezone

from etc.models.bases import IDTimeBaseModel, UUIDTimeBaseModel


class GameChatRoom(UUIDTimeBaseModel):
    class Meta:
        verbose_name = "Чат комната"
        verbose_name_plural = "Чат комнаты"

    game = models.OneToOneField(
        "game.Game",
        on_delete=models.CASCADE,
        related_name="chat_room",
        verbose_name="Игра",
    )
    is_active = models.BooleanField("Активен", default=True)
    archived_at = models.DateTimeField("Дата архивации", null=True, blank=True)

    def __str__(self):
        return f"Чат игры: {self.game.title}"
    

class ChatMembership(IDTimeBaseModel):
    class Meta:
        verbose_name = "Участник чата"
        verbose_name_plural = "Участники чата"

    user = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="chat_membership",
        verbose_name="Пользователь",
    )
    room = models.ForeignKey(
        "chat.GameChatRoom",
        on_delete=models.CASCADE,
        related_name="memeberships",
        verbose_name="Комната",
    )
    joined_at = models.DateTimeField(
        "Дата присоединения",
        auto_now_add=True,
    )
    last_read_at = models.DateTimeField(
        "Послднее прочтение",
        default=timezone.now(),
    )
    is_muted = models.BooleanField(
        "Заглушен",
        default=False,
    )
    #TODO: подумать над role в чате???

    def __str__(self):
        return f"{self.user.email} в {self.room}"


class ChatMessage(UUIDTimeBaseModel):
    class Meta:
        verbose_name = "Сообщение чата"
        verbose_name_plural = "Сообщения чата"
    
    room = models.ForeignKey(
        "chat.GameChatRoom",
        on_delete=models.CASCADE,
        related_name="message",
        verbose_name="Комната",
    )
    sender = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="chat_message",
        verbose_name="Отправитель",
    )
    text = models.TextField("Текст сообщения")

    def __str__(self):
        return f"Сообщение от {self.sender.email} в {self.room}"