# Water intake logic and HTTP endpoints are defined here so they can be reused
# by both the FastAPI app and the MCP tool registrations.

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="", tags=["fitness"])


# --- Pydantic model ----------------------------------------------------------

class WaterIntakeRequest(BaseModel):
    weight_kg: float = Field(..., gt=0, description="Body weight in kg, must be greater than 0")
    workout_minutes: int = Field(..., ge=0, description="Workout duration in minutes, must be >= 0")


# --- Core logic function -----------------------------------------------------

def calculate_water_intake_value(weight_kg: float, workout_minutes: int) -> dict:
    """
    Calculate daily water intake target based on weight and workout duration.

    Args:
        weight_kg: User's body weight in kilograms.
        workout_minutes: Duration of workout in minutes.

    Returns:
        Dictionary with daily water target and breakdown.
    """
    request = WaterIntakeRequest(weight_kg=weight_kg, workout_minutes=workout_minutes)

    # Base intake (0.025L per kg of body weight)
    base_litres = request.weight_kg * 0.025

    # Additional intake (1L per 60 minutes of workout)
    exercise_litres = request.workout_minutes / 60

    total_litres = round(base_litres + exercise_litres, 2)

    return {
        "weight_kg": request.weight_kg,
        "workout_minutes": request.workout_minutes,
        "base_intake_litres": round(base_litres, 2),
        "exercise_intake_litres": round(exercise_litres, 2),
        "total_daily_target_litres": total_litres,
        "recommendation": f"Drink at least {total_litres}L of water today.",
    }


# --- FastAPI endpoint ---------------------------------------------------------

@router.post("/calculate-water-intake", operation_id="calculate_water_intake")
def calculate_water_intake(weight_kg: float, workout_minutes: int):
    """
    HTTP endpoint: calculate daily water intake.

    Args:
        weight_kg: User's body weight in kilograms.
        workout_minutes: Duration of workout in minutes.

    Returns:
        JSON dict with the water intake breakdown.
    """
    return calculate_water_intake_value(weight_kg=weight_kg, workout_minutes=workout_minutes)


# --- Metadata for MCP tool registration --------------------------------------

TOOL_DEFINITIONS = [
    {
        "name": "calculate_water_intake",
        "description": "Calculate daily water intake target based on body weight and workout duration.",
        "func": calculate_water_intake_value,
        "tags": {"fitness", "hydration"},
    },
]