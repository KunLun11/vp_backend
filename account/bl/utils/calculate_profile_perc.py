from account.models.profiles import PlayerProfile


def calculate_profile_percentage(profile: PlayerProfile) -> int:
    fileds_to_check = [
        profile.first_name,
        profile.last_name,
        profile.middle_name,
        profile.birth_date,
        profile.city,          
        profile.photo,
        profile.skill_level,
        profile.position,
    ]
    filled_count = 0
    for field in fileds_to_check:
        if field:
            filled_count += 1
    return int(filled_count * 12.5)