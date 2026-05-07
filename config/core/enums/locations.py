from django.db import models


class VenueType(models.IntegerChoices):
    sport_complex = 1, "Спортивный комплекс"
    school_gym = 2, "Школьный зал"
    university_gym = 3, "Университетский зал"
    private_club = 4, "Частный клуб"
    outdoor = 5, "Открытая площадка"
    beach = 6, "Пляж"


class SurfaceType(models.IntegerChoices):
    parquet = 1, "Паркет"
    synthetic = 2, "Синтетика"
    sand = 3, "Песок"
    concrete = 4, "Бетон"
    rubber = 5, "Резина"
    other = 6, "Другое"


