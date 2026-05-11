# Sweat loss logic and HTTP endpoints (v2 - API Ninjas) are defined here so
# they can be reused by both the FastAPI app and the MCP tool registrations.

import os
import httpx
from dotenv import load_dotenv

from fastapi import APIRouter
from pydantic import BaseModel, Field

load_dotenv()

router = APIRouter(prefix="", tags=["fitness"])

API_KEY = os.getenv("API_NINJAS_KEY")
API_URL = "https://api.api-ninjas.com/v1/nutrition"

# Recovery foods by intensity level (5 foods each)
RECOVERY_FOODS = {
    "low": ["banana", "orange", "watermelon", "yogurt", "milk"],
    "moderate": ["sweet potato", "banana", "eggs", "brown rice", "avocado"],
    "high": ["salted nuts", "protein bar", "chocolate milk", "quinoa", "salmon"],
}


# --- Pydantic model ----------------------------------------------------------

class SweatLossV2Request(BaseModel):
    workout_duration_min: int = Field(..., ge=1, le=480, description="Workout duration in minutes, 1-480")
    intensity_level: str = Field(..., description="Intensity level: low, moderate, or high")


# --- Core logic function -----------------------------------------------------

def estimate_sweat_loss_v2_value(workout_duration_min: int, intensity_level: str) -> dict:
    """
    Estimate fluid and mineral loss during a workout.
    Fetches recovery food nutrition data from API Ninjas (Version 2).

    Args:
        workout_duration_min: Duration of workout in minutes.
        intensity_level: Intensity of workout - low, moderate, or high.

    Returns:
        Dictionary with fluid and mineral loss estimates and recovery food data.
    """
    request = SweatLossV2Request(
        workout_duration_min=workout_duration_min,
        intensity_level=intensity_level,
    )

    rates = {"low": 0.5, "moderate": 1.0, "high": 1.5}

    if request.intensity_level.lower() not in rates:
        raise ValueError(
            f"Invalid intensity '{request.intensity_level}'. Choose: low, moderate, high"
        )

    sweat_rate = rates[request.intensity_level.lower()]
    litres_lost = round((request.workout_duration_min / 60) * sweat_rate, 2)

    sodium_lost = round(litres_lost * 900, 1)
    potassium_lost = round(litres_lost * 200, 1)
    magnesium_lost = round(litres_lost * 36, 1)

    # Fetch recovery food nutrition data from API Ninjas
    foods_to_lookup = RECOVERY_FOODS[request.intensity_level.lower()]
    headers = {"X-Api-Key": API_KEY}
    recovery_foods_data = []

    for food_name in foods_to_lookup:
        try:
            response = httpx.get(
                API_URL,
                headers=headers,
                params={"query": food_name},
                timeout=10,
            )
            response.raise_for_status()
            nutrition_data = response.json()

            if nutrition_data:
                food = nutrition_data[0]
                recovery_foods_data.append({
                    "food": food.get("name", food_name),
                    "potassium_mg": food.get("potassium_mg", 0),
                    "sodium_mg": food.get("sodium_mg", 0),
                    "magnesium_mg": food.get("magnesium_mg", 0),
                })
            else:
                recovery_foods_data.append({"food": food_name, "error": "No data found"})

        except Exception as exc:
            recovery_foods_data.append({"food": food_name, "error": str(exc)})

    return {
        "version": "v2 - API Ninjas",
        "workout_duration_min": request.workout_duration_min,
        "intensity_level": request.intensity_level.lower(),
        "fluid_lost_litres": litres_lost,
        "sodium_lost_mg": sodium_lost,
        "potassium_lost_mg": potassium_lost,
        "magnesium_lost_mg": magnesium_lost,
        "recommended_replacement_litres": round(litres_lost * 1.5, 2),
        "recovery_foods": recovery_foods_data,
        "data_source": "API Ninjas Nutrition API",
    }


# --- FastAPI endpoint ---------------------------------------------------------

@router.post("/estimate-sweat-loss-v2", operation_id="estimate_sweat_loss_v2")
def estimate_sweat_loss_v2(workout_duration_min: int, intensity_level: str):
    """
    HTTP endpoint: estimate sweat and mineral loss with recovery food data (v2 - API Ninjas).

    Args:
        workout_duration_min: Duration of workout in minutes.
        intensity_level: Intensity level - low, moderate, or high.

    Returns:
        JSON dict with fluid and mineral loss estimates and recovery food data.
    """
    try:
        return estimate_sweat_loss_v2_value(
            workout_duration_min=workout_duration_min,
            intensity_level=intensity_level,
        )
    except ValueError as exc:
        return {"error": str(exc), "operation": "estimate_sweat_loss_v2"}


# --- Metadata for MCP tool registration --------------------------------------

TOOL_DEFINITIONS = [
    {
        "name": "estimate_sweat_loss_v2",
        "description": "Estimate fluid and mineral loss with real recovery food data from API Ninjas. (v2 - API)",
        "func": estimate_sweat_loss_v2_value,
        "tags": {"fitness", "sweat", "minerals", "nutrition"},
    },
]