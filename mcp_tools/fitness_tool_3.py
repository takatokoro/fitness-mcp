"""Tool 3 — Weather-Adjusted Hydration Calculator.

Accepts a city name (e.g. "Perth") instead of raw coordinates.
Geocoding is handled by services/weather_service.py via the free
Open-Meteo geocoding API — no API key required.
After each call, updates the weather_context resource in memory
so Prompt 3 (ai_fitness_summary) can read current conditions.
"""

import logging

from fastapi import APIRouter
from pydantic import BaseModel, Field

from services.weather_service import get_coordinates, get_current_weather
from mcp_resources.fitness_resources import update_weather_context

logger = logging.getLogger(__name__)

router = APIRouter(prefix="", tags=["fitness"])


# --- Pydantic model ----------------------------------------------------------

class WeatherHydrationRequest(BaseModel):
    weight_kg: float = Field(..., gt=0, description="Body weight in kg, must be greater than 0")
    workout_minutes: int = Field(..., ge=0, description="Workout duration in minutes, must be >= 0")
    city: str = Field(..., description="City name e.g. Perth, Tokyo, London, New York")


# --- Core logic function -----------------------------------------------------

def weather_adjusted_hydration_value(
    weight_kg: float,
    workout_minutes: int,
    city: str,
) -> dict:
    """
    Calculate weather-adjusted daily water intake target from a city name.

    Steps:
      1. Geocode city name -> coordinates (Open-Meteo geocoding, free)
      2. Fetch live weather at those coordinates (Open-Meteo forecast, free)
      3. Apply hydration formula with weather adjustments
      4. Update weather_context resource in memory

    Base formula (from Tool 1):
      - 0.025L per kg body weight
      - 1L per 60 minutes of exercise

    Weather adjustments:
      - Temperature above 25C: +0.1L per degree above 25
      - Humidity above 60%: +0.2L flat bonus
    """
    request = WeatherHydrationRequest(
        weight_kg=weight_kg,
        workout_minutes=workout_minutes,
        city=city,
    )

    # Step 1 - Geocode city to coordinates
    coords = get_coordinates(request.city)

    # Step 2 - Fetch live weather
    weather = get_current_weather(coords["latitude"], coords["longitude"])
    temperature = weather["temperature_celsius"]
    humidity = weather["relative_humidity_percent"]

    # Step 3 - Base intake (same formula as Tool 1)
    base_litres = round(request.weight_kg * 0.025, 2)
    exercise_litres = round(request.workout_minutes / 60, 2)
    base_total = round(base_litres + exercise_litres, 2)

    # Weather adjustments
    heat_adjustment = 0.0
    if temperature > 25:
        heat_adjustment = round((temperature - 25) * 0.1, 2)

    humidity_adjustment = 0.2 if humidity > 60 else 0.0

    total_adjustment = round(heat_adjustment + humidity_adjustment, 2)
    adjusted_total = round(base_total + total_adjustment, 2)

    # Step 4 - Update weather_context resource for Prompt 3
    update_weather_context(
        city=coords["resolved_city"],
        temperature_celsius=temperature,
        humidity_percent=humidity,
    )

    logger.info(
        "Weather hydration [%s]: base=%.2fL, heat_adj=%.2fL, humidity_adj=%.2fL, total=%.2fL",
        coords["resolved_city"], base_total, heat_adjustment, humidity_adjustment, adjusted_total,
    )

    return {
        "weight_kg": request.weight_kg,
        "workout_minutes": request.workout_minutes,
        "location": {
            "input_city": request.city,
            "resolved_city": coords["resolved_city"],
            "country": coords["country"],
            "latitude": coords["latitude"],
            "longitude": coords["longitude"],
        },
        "base_intake_litres": base_litres,
        "exercise_intake_litres": exercise_litres,
        "base_total_litres": base_total,
        "weather": weather,
        "heat_adjustment_litres": heat_adjustment,
        "humidity_adjustment_litres": humidity_adjustment,
        "total_adjustment_litres": total_adjustment,
        "adjusted_daily_target_litres": adjusted_total,
        "recommendation": (
            f"Drink at least {adjusted_total}L today in {coords['resolved_city']}. "
            f"({temperature}\u00b0C, {humidity}% humidity)"
        ),
    }


# --- FastAPI endpoint ---------------------------------------------------------

@router.post("/weather-adjusted-hydration", operation_id="weather_adjusted_hydration")
def weather_adjusted_hydration(
    weight_kg: float,
    workout_minutes: int,
    city: str,
):
    """
    HTTP endpoint: calculate weather-adjusted daily water intake.

    Args:
        weight_kg: Body weight in kilograms.
        workout_minutes: Workout duration in minutes.
        city: City name e.g. Perth, Tokyo, London, New York.

    Returns:
        JSON dict with resolved location, weather data, adjustments, and final target.
    """
    try:
        return weather_adjusted_hydration_value(
            weight_kg=weight_kg,
            workout_minutes=workout_minutes,
            city=city,
        )
    except ValueError as exc:
        return {"error": str(exc), "operation": "weather_adjusted_hydration"}
    except Exception as exc:
        return {"error": str(exc), "operation": "weather_adjusted_hydration"}


# --- Metadata for MCP tool registration --------------------------------------

TOOL_DEFINITIONS = [
    {
        "name": "weather_adjusted_hydration",
        "description": (
            "Calculate daily water intake adjusted for live weather (temperature and humidity). "
            "Accepts a city name (e.g. Perth, Tokyo, London) — no coordinates needed."
        ),
        "func": weather_adjusted_hydration_value,
        "tags": {"fitness", "hydration", "weather"},
    },
]
