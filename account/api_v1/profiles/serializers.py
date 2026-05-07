from rest_framework import serializers

from account.models.profiles import PlayerProfile


class PlayerProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    skill_level_display = serializers.CharField(source="get_skill_level_display", read_only=True)
    position_display = serializers.CharField(source="get_position_display", read_only=True)

    class Meta:
        model = PlayerProfile
        fields = "__all__"
        read_only_fields = [
            "id",
            "user",
            "completion_percentage",
            "total_games",
            "total_tournament",
            "elo_rating",
            "classic_rating",
            "created_at",
            "updated_at",
        ]

    def get_user(self, obj):
        return {
            "id": str(obj.user.pk),
            "email": obj.user.email,
            "role": obj.user.role,
        }

    def _calculate_completion(self, profile):
        fields = [
            profile.first_name,
            profile.last_name,
            profile.middle_name,
            profile.birth_date,
            profile.city,
            profile.photo,
            profile.skill_level,
            profile.position,
        ]
        filled = sum(1 for f in fields if f)
        return int(filled * 12.5)

    def validate(self, data):
        if self.context["request"].method == "POST":
            if PlayerProfile.objects.filter(user=self.context["request"].user).exists():
                raise serializers.ValidationError("Профиль уже существует")
        return data

    def create(self, validated_data):
        profile = PlayerProfile.objects.create(**validated_data)
        profile.completion_percentage = self._calculate_completion(profile)
        profile.save(update_fields=["completion_percentage"])
        return profile

    def update(self, instance, validated_data):
        if "photo" in validated_data and instance.photo:
            instance.photo.delete(save=False)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.completion_percentage = self._calculate_completion(instance)
        instance.save()
        return instance
