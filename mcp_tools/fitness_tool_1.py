"""MCP Tool 1 - Calculate Water Intake with Pydantic validation."""

from pydantic import BaseModel, Field


class WaterIntakeRequest(BaseModel):
    weight_kg: float = Field(..., gt=0, description="Body weight in kg, must be greater than 0")
    workout_minutes: int = Field(..., ge=0, description="Workout duration in minutes, must be greater than 0")


def calculate_water_intake(weight_kg: float, workout_minutes: int) -> dict:
    """
    Calculate daily water intake target based on weight and workout duration.

    User Input:
        weight_kg: User's body weight in kilograms.
        workout_minutes: Duration of workout in minutes.

    Returns:
        Dictionary with daily water target and breakdown.
    """
    # Validate using Pydantic
    request = WaterIntakeRequest(weight_kg=weight_kg, workout_minutes=workout_minutes)

    # Base intake (0.025L per kg of body weight)
    base_litres = request.weight_kg * 0.025

    # Additional intake (1L per 60 minutes workout)
    exercise_litres = request.workout_minutes / 60

    total_litres = round(base_litres + exercise_litres, 2)

    return {
        "weight_kg": request.weight_kg,
        "workout_minutes": request.workout_minutes,
        "base_intake_litres": round(base_litres, 2),
        "exercise_intake_litres": round(exercise_litres, 2),
        "total_daily_target_litres": total_litres,
        "recommendation": f"Drink at least {total_litres}L of water today."
    }