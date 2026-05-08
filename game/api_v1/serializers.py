from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from account.models.profiles import OrganizerProfile, PlayerProfile
from config.core.enums.games import ParticipantStatus
from etc.models.location import Location
from game.bl.organizers import GameOrganizerService
from game.bl.players import GamePlayerService
from game.models import Game, GameParticipant


class OrganizerShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizerProfile
        fields = ["id", "first_name", "last_name", "photo"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "name", "address", "city", "latitude", "longitude", "venue_type", "surface_type"]


class PlayerShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerProfile
        fields = ["id", "first_name", "last_name", "photo"]


class GameListSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    available_slots = serializers.SerializerMethodField()
    skill_level_display = serializers.CharField(source="get_skill_level_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Game
        fields = [
            "id",
            "title",
            "location",
            "date_time",
            "duration_minutes",
            "booked_count",
            "capacity",
            "price",
            "skill_level",
            "skill_level_display",
            "status",
            "status_display",
            "gender",
            "available_slots",
        ]

    @extend_schema_field(serializers.IntegerField)
    def get_available_slots(self, obj):
        return obj.get_available_slots()


class GameDetailSerializer(GameListSerializer):
    organizer = OrganizerShortSerializer(read_only=True)
    is_participant = serializers.SerializerMethodField()

    class Meta(GameListSerializer.Meta):
        fields = GameListSerializer.Meta.fields + [
            "organizer",
            "description",
            "is_tournament",
            "elo_rating_change",
            "created_at",
            "updated_at",
            "is_participant",
        ]

    def get_is_participant(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        try:
            return GameParticipant.objects.filter(
                game=obj,
                player__user=request.user,
                status__in=[ParticipantStatus.registered, ParticipantStatus.confirmed],
            ).exists()
        except PlayerProfile.DoesNotExist:
            return False


class CreateGameSerializer(serializers.ModelSerializer):
    location_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Game
        fields = [
            "location_id",
            "title",
            "date_time",
            "duration_minutes",
            "capacity",
            "price",
            "skill_level",
            "gender",
            "status",
            "is_tournament",
            "description",
        ]

    def validate_location_id(self, value):
        if not Location.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Указанная локация не найдена")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        return GameOrganizerService.create_game(user, validated_data)


class PublishGameSerializer(serializers.Serializer):
    def save(self, **kwargs):
        request = self.context["request"]
        game_id = self.context["game_id"]
        return GameOrganizerService.publish_game(request.user, game_id)


class CloseRegistrationSerializer(serializers.Serializer):
    def save(self, **kwargs):
        request = self.context["request"]
        game_id = self.context["game_id"]
        return GameOrganizerService.close_registration(request.user, game_id)


class CompleteGameSerializer(serializers.Serializer):
    def save(self, **kwargs):
        request = self.context["request"]
        game_id = self.context["game_id"]
        return GameOrganizerService.complete_game(request.user, game_id)


class CancelGameSerializer(serializers.Serializer):
    def save(self, **kwargs):
        request = self.context["request"]
        game_id = self.context["game_id"]
        return GameOrganizerService.cancel_game(request.user, game_id)


class RegisterOnGameSerializer(serializers.Serializer):
    def save(self, **kwargs):
        request = self.context["request"]
        game_id = self.context["game_id"]
        return GamePlayerService.register_player(request.user.pk, game_id)


class CancelRegistrationSerializer(serializers.Serializer):
    def save(self, **kwargs):
        request = self.context["request"]
        game_id = self.context["game_id"]
        return GamePlayerService.cancel_registration(request.user.pk, game_id)


class ConfirmParticipantSerializer(serializers.Serializer):
    def save(self, **kwargs):
        request = self.context["request"]
        game_id = self.context["game_id"]
        return GamePlayerService.confirm_participant(request.user.pk, game_id)


class AttendSerializer(serializers.Serializer):
    def save(self, **kwargs):
        request = self.context["request"]
        game_id = self.context["game_id"]
        return GamePlayerService.mark_attended(request.user.pk, game_id)


class NoShowSerializer(serializers.Serializer):
    participant_id = serializers.IntegerField(write_only=True)

    def save(self, **kwargs):
        request = self.context["request"]
        game_id = self.context["game_id"]
        return GamePlayerService.mark_no_show(request.user, game_id, self.validated_data["participant_id"])


class GameParticipantSerializer(serializers.ModelSerializer):
    player = PlayerShortSerializer(read_only=True)
    game = serializers.PrimaryKeyRelatedField(read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = GameParticipant
        fields = ["id", "game", "player", "status", "status_display", "registered_at", "cancelled_at", "checked_in_at"]


class MyGameParticipantSerializer(serializers.ModelSerializer):
    game = GameDetailSerializer(read_only=True)
    participant_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = GameParticipant
        fields = ["participant_id", "game", "status", "registered_at"]
