"""MCP Tool 1 for the Personal Fitness Assistant."""


def calculate_water_intake(weight_kg: float, workout_minutes: int) -> dict:
    """
    Calculate daily water intake target based on weight and workout duration.

    Args:
        weight_kg: User's body weight in kilograms.
        workout_minutes: Duration of workout in minutes.

    Returns:
        Dictionary with daily water target and breakdown.
    """
    # Base intake: 35ml per kg of body weight
    base_litres = (weight * 35) / 1000        # BUG: should be weight_kg

    # Additional intake for exercise: 500ml per 30 mins of workout
    exercise_litres = (workout_minutes / 30) * 0.5

    total_litres = round(base_litres + exercise_litres, 2)

    return {
        "weight_kg": weight_kg,
        "workout_minutes": workout_minutes,
        "base_intake_litres": round(base_litres, 2),
        "exercise_intake_litres": round(exercise_litres, 2),
        "total_daily_target_litres": total_litres,
        "recommendation": f"Drink at least {total_litres}L of water today."
    }


TOOL_DEFINITIONS = [
    {
        "name": "calculate_water_intake",
        "description": "Calculate daily water intake target based on body weight and workout duration.",
        "func": calculate_water_intake,
    },
]