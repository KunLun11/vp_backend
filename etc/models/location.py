from django.db import models

from config.core.enums.locations import SurfaceType, VenueType
from etc.models.bases import IDTimeBaseModel


class Location(IDTimeBaseModel):
    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"
        indexes = [
            models.Index(fields=["latitude", "longitude"]),
        ]

    name = models.CharField("Название зала", max_length=200)
    address = models.CharField("Адрес", max_length=500)
    city = models.CharField("Город", max_length=100)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Широта",
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Долгота",
    )
    venue_type = models.PositiveSmallIntegerField(
        "Тип зала",
        choices=VenueType.choices,
    )
    surface_type = models.PositiveSmallIntegerField(
        "Покрытие",
        null=True,
        blank=True,
        choices=SurfaceType.choices,
    )
    contact_phone = models.CharField("Телефон", max_length=20, null=True, blank=True)
    contact_email = models.EmailField("Email", null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.city})"
