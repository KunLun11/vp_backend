from django.db import models

from config.core.enums.users import Gender
from etc.models.bases import IDTimeBaseModel


class BaseProfile(IDTimeBaseModel):
    class Meta:
        abstract = True

    first_name = models.CharField("Имя", max_length=120, blank=True, default="")
    last_name = models.CharField("Фамилия", max_length=120, blank=True, default="")
    middle_name = models.CharField("Отчество", max_length=120, blank=True, default="")
    birth_date = models.DateField("Дата рождения")
    gender = models.CharField(
        "Пол",
        max_length=10,
        choices=Gender.choices,
    )
    city = models.CharField("Город", max_length=100)
    elo_rating = models.IntegerField("ELO рейтинг", default=700)
    classic_rating = models.DecimalField(
        "Классический рейтинг",
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
    )
    photo = models.ImageField(
        "Фото профиля",
        upload_to="profiles/",
    )

    def __str__(self):
        return f"{self.pk} {self.last_name} {self.first_name} {self.middle_name}"
