"""MCP Tool 1 - Calculate Water Intake."""


def calculate_water_intake(weight_kg: float, workout_minutes: int) -> dict:
    """
    Calculate daily water intake target based on weight and workout duration.

    User's Input:
        weight_kg: User's body weight in kilograms.
        workout_minutes: Duration of workout in minutes.

    Returns:
        Dictionary with daily water target and breakdown.
    """
    # Base intake (0.028L per kg of body weight)
    base_litres = weight_kg * 0.028

    # Additional intake (1L per 60 minutes workout)
    exercise_litres = workout_minutes / 60

    total_litres = round(base_litres + exercise_litres, 2)

    # BUG: returning wrong key name - "daily_target" instead of "total_daily_target_litres"
    return {
        "weight_kg": weight_kg,
        "workout_minutes": workout_minutes,
        "base_intake_litres": round(base_litres, 2),
        "exercise_intake_litres": round(exercise_litres, 2),
        "tota_daily_target_intake": total_litres,
        "recommendation": f"Drink at least {total_litres}L of water today."
    }