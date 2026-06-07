"""Tool 3 — Weather-Adjusted Hydration Calculator.

Calls Open-Meteo via services/weather_service.py to get live temperature
and humidity, then adjusts the base hydration target accordingly.
Follows the same pattern as fitness_tool_1.py and fitness_tool_2_v1.py.
"""

import logging

from fastapi import APIRouter
from pydantic import BaseModel, Field

from services.weather_service import get_current_weather

logger = logging.getLogger(__name__)

router = APIRouter(prefix="", tags=["fitness"])


# --- Pydantic model ----------------------------------------------------------

class WeatherHydrationRequest(BaseModel):
    weight_kg: float = Field(..., gt=0, description="Body weight in kg, must be greater than 0")
    workout_minutes: int = Field(..., ge=0, description="Workout duration in minutes, must be >= 0")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude of workout location")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude of workout location")


# --- Core logic function -----------------------------------------------------

def weather_adjusted_hydration_value(
    weight_kg: float,
    workout_minutes: int,
    latitude: float,
    longitude: float,
) -> dict:
    """
    Calculate weather-adjusted daily water intake target.

    Base formula (from Tool 1):
      - 0.025L per kg body weight
      - 1L per 60 minutes of exercise

    Weather adjustments:
      - Temperature above 25°C: +0.1L per degree above 25
      - Humidity above 60%: +0.2L flat bonus

    Args:
        weight_kg: User's body weight in kilograms.
        workout_minutes: Duration of workout in minutes.
        latitude: Latitude of the user's location.
        longitude: Longitude of the user's location.

    Returns:
        Dictionary with base target, weather data, adjustments, and final target.
    """
    request = WeatherHydrationRequest(
        weight_kg=weight_kg,
        workout_minutes=workout_minutes,
        latitude=latitude,
        longitude=longitude,
    )

    # Base intake (same formula as Tool 1)
    base_litres = round(request.weight_kg * 0.025, 2)
    exercise_litres = round(request.workout_minutes / 60, 2)
    base_total = round(base_litres + exercise_litres, 2)

    # Fetch live weather
    weather = get_current_weather(request.latitude, request.longitude)
    temperature = weather["temperature_celsius"]
    humidity = weather["relative_humidity_percent"]

    # Weather adjustments
    heat_adjustment = 0.0
    if temperature > 25:
        heat_adjustment = round((temperature - 25) * 0.1, 2)

    humidity_adjustment = 0.2 if humidity > 60 else 0.0

    total_adjustment = round(heat_adjustment + humidity_adjustment, 2)
    adjusted_total = round(base_total + total_adjustment, 2)

    logger.info(
        "Weather hydration: base=%.2fL, heat_adj=%.2fL, humidity_adj=%.2fL, total=%.2fL",
        base_total, heat_adjustment, humidity_adjustment, adjusted_total,
    )

    return {
        "weight_kg": request.weight_kg,
        "workout_minutes": request.workout_minutes,
        "latitude": request.latitude,
        "longitude": request.longitude,
        "base_intake_litres": base_litres,
        "exercise_intake_litres": exercise_litres,
        "base_total_litres": base_total,
        "weather": weather,
        "heat_adjustment_litres": heat_adjustment,
        "humidity_adjustment_litres": humidity_adjustment,
        "total_adjustment_litres": total_adjustment,
        "adjusted_daily_target_litres": adjusted_total,
        "recommendation": (
            f"Drink at least {adjusted_total}L today. "
            f"({temperature}°C, {humidity}% humidity at your location)"
        ),
    }


# --- FastAPI endpoint ---------------------------------------------------------

@router.post("/weather-adjusted-hydration", operation_id="weather_adjusted_hydration")
def weather_adjusted_hydration(
    weight_kg: float,
    workout_minutes: int,
    latitude: float,
    longitude: float,
):
    """
    HTTP endpoint: calculate weather-adjusted daily water intake.

    Args:
        weight_kg: Body weight in kilograms.
        workout_minutes: Workout duration in minutes.
        latitude: Latitude of workout location.
        longitude: Longitude of workout location.

    Returns:
        JSON dict with base intake, weather data, adjustments, and final target.
    """
    try:
        return weather_adjusted_hydration_value(
            weight_kg=weight_kg,
            workout_minutes=workout_minutes,
            latitude=latitude,
            longitude=longitude,
        )
    except Exception as exc:
        return {"error": str(exc), "operation": "weather_adjusted_hydration"}


# --- Metadata for MCP tool registration --------------------------------------

TOOL_DEFINITIONS = [
    {
        "name": "weather_adjusted_hydration",
        "description": (
            "Calculate daily water intake adjusted for live weather (temperature and humidity). "
            "Requires weight, workout minutes, and location coordinates."
        ),
        "func": weather_adjusted_hydration_value,
        "tags": {"fitness", "hydration", "weather"},
    },
]
