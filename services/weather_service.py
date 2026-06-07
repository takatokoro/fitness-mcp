"""Weather service wrapper for Open-Meteo API.

All external weather API calls live here, never inside tool or route files.
Open-Meteo is free and requires no API key.
"""

import logging
import httpx

logger = logging.getLogger(__name__)

BASE_URL = "https://api.open-meteo.com/v1/forecast"


def get_current_weather(latitude: float, longitude: float) -> dict:
    """
    Fetch current temperature and humidity from Open-Meteo.

    Args:
        latitude: Location latitude.
        longitude: Location longitude.

    Returns:
        Dictionary with temperature_celsius and relative_humidity_percent.
        Falls back to defaults (20°C, 50%) if the API call fails.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
        "hourly": "relativehumidity_2m",
    }

    try:
        response = httpx.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        temperature = data.get("current_weather", {}).get("temperature", 20.0)

        # Hourly humidity - take the first available reading
        hourly = data.get("hourly", {})
        humidity_list = hourly.get("relativehumidity_2m", [50])
        humidity = humidity_list[0] if humidity_list else 50

        logger.info(
            "Weather fetched: %.1f°C, %d%% humidity at (%.4f, %.4f)",
            temperature, humidity, latitude, longitude,
        )

        return {
            "temperature_celsius": temperature,
            "relative_humidity_percent": humidity,
            "source": "Open-Meteo",
        }

    except Exception as exc:
        logger.warning("Weather API call failed: %s — using fallback defaults.", exc)
        return {
            "temperature_celsius": 20.0,
            "relative_humidity_percent": 50,
            "source": "fallback_defaults",
            "warning": f"Weather API unavailable: {str(exc)}",
        }
