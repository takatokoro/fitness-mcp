"""MCP Tool 2 (version 2) - Estimate Sweat Loss (Version 2 - API Ninjas)."""

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_NINJAS_KEY")
API_URL = "https://api.api-ninjas.com/v1/nutrition"

# Recovery foods by intensity level (5 foods each)
RECOVERY_FOODS = {
    "low": ["banana", "orange", "watermelon", "yogurt", "milk"],
    "moderate": ["sweet potato", "banana", "eggs", "brown rice", "avocado"],
    "high": ["salted nuts", "protein bar", "chocolate milk", "quinoa", "salmon"]
}


def estimate_sweat_loss_v2(workout_duration_min: int, intensity_level: str) -> dict:
    """
    Estimate fluid and mineral loss during a workout.
    Fetches recovery food nutrition data from API Ninjas (Version 2).

    Args:
        workout_duration_min: Duration of workout in minutes.
        intensity_level: Intensity of workout - low, moderate, or high.

    Returns:
        Dictionary with fluid and mineral loss estimates and real recovery food data.
    """
    rates = {"low": 0.5, "moderate": 1.0, "high": 1.5}

    if intensity_level.lower() not in rates:
        raise ValueError(
            f"Invalid intensity '{intensity_level}'. Choose: low, moderate, high"
        )

    sweat_rate = rates[intensity_level.lower()]
    litres_lost = round((workout_duration_min / 60) * sweat_rate, 2)

    sodium_lost = round(litres_lost * 900, 1)
    potassium_lost = round(litres_lost * 200, 1)
    magnesium_lost = round(litres_lost * 36, 1)

    # Get recovery foods for this intensity level
    foods_to_lookup = RECOVERY_FOODS[intensity_level.lower()]
    headers = {"X-Api-Key": API_KEY}

    recovery_foods_data = []

    for food_name in foods_to_lookup:
        try:
            response = httpx.get(
                API_URL,
                headers=headers,
                params={"query": food_name},
                timeout=10
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
                recovery_foods_data.append({
                    "food": food_name,
                    "error": "No data found"
                })

        except Exception as e:
            recovery_foods_data.append({
                "food": food_name,
                "error": str(e)
            })

    return {
        "version": "v2 - API Ninjas",
        "workout_duration_min": workout_duration_min,
        "intensity_level": intensity_level.lower(),
        "fluid_lost_litres": litres_lost,
        "sodium_lost_mg": sodium_lost,
        "potassium_lost_mg": potassium_lost,
        "magnesium_lost_mg": magnesium_lost,
        "recommended_replacement_litres": round(litres_lost * 1.5, 2),
        "recovery_foods": recovery_foods_data,
        "data_source": "API Ninjas Nutrition API"
    }