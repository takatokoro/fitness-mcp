"""MCP Tool 2 - Estimate Sweat Loss."""


def estimate_sweat_loss(workout_duration_min: int, intensity_level: str) -> dict:
    """
    Estimate fluid and mineral loss during a workout.

    User's input:
        workout_duration_min: Duration of workout in minutes.
        intensity_level: Intensity of workout - low, moderate, or high.

    Returns:
        Dictionary with fluid and mineral loss estimates.
    """
    rates = {"low": 0.5, "moderate": 1.0, "high": 1.5}

    if intensity_level.lower() not in rates:
        raise ValueError(f"Invalid intensity '{intensity_level}'. Choose: low, moderate, high")

    sweat_rate = rates[intensity_level.lower()]
    litres_lost = round((workout_duration_min / 60) * sweat_rate, 2)

    return {
        "workout_duration_min": workout_duration_min,
        "intensity_level": intensity_level,
        "fluid_lost_litres": litres_lost,
        "sodium_lost_mg": round(litres_lost * 900, 1),
        "potassium_lost_mg": round(litres_lost * 200, 1),
        "magnesium_lost_mg": round(litres_lost * 36, 1),
        "recommended_replacement_litres": round(litres_lost * 1.5, 2)
    }