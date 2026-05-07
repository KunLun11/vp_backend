import django_filters

from config.core.enums.games import GameStatus
from config.core.enums.users import SkillLevel
from game.models import Game


class GameFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    status = django_filters.ChoiceFilter(choices=GameStatus.choices)
    skill_level = django_filters.ChoiceFilter(choices=SkillLevel.choices)
    gender = django_filters.NumberFilter()
    date_from = django_filters.DateTimeFilter(field_name="date_time", lookup_expr="gte")
    date_to = django_filters.DateTimeFilter(field_name="date_time", lookup_expr="lte")

    class Meta:
        model = Game
        fields = ["title", "status", "skill_level", "gender", "date_from", "date_to"]
