"""Tests for Tool 3 — Weather-Adjusted Hydration (geocoding + weather mocked)."""

from unittest.mock import patch
from mcp_tools.fitness_tool_3 import weather_adjusted_hydration_value

# Mock geocoding response — replaces real Open-Meteo geocoding call
MOCK_COORDS = {
    "latitude": -31.95,
    "longitude": 115.86,
    "resolved_city": "Perth",
    "country": "Australia",
}

# Mock weather responses
MOCK_WEATHER_HOT = {
    "temperature_celsius": 35.0,   # 10° above 25 → +1.0L heat adjustment
    "relative_humidity_percent": 80,  # above 60% → +0.2L humidity adjustment
    "source": "Open-Meteo",
}

MOCK_WEATHER_MILD = {
    "temperature_celsius": 20.0,   # below 25 → no heat adjustment
    "relative_humidity_percent": 40,  # below 60% → no humidity adjustment
    "source": "Open-Meteo",
}


def test_hot_weather_increases_target():
    with patch("mcp_tools.fitness_tool_3.get_coordinates", return_value=MOCK_COORDS), \
         patch("mcp_tools.fitness_tool_3.get_current_weather", return_value=MOCK_WEATHER_HOT):
        result = weather_adjusted_hydration_value(
            weight_kg=70, workout_minutes=60, city="Perth"
        )
    # Base: (70*0.025) + (60/60) = 1.75 + 1.0 = 2.75
    # Heat: (35-25)*0.1 = 1.0, Humidity: 0.2 → total adj = 1.2
    # Adjusted: 2.75 + 1.2 = 3.95
    assert result["adjusted_daily_target_litres"] == 3.95
    assert result["heat_adjustment_litres"] == 1.0
    assert result["humidity_adjustment_litres"] == 0.2


def test_mild_weather_no_adjustment():
    with patch("mcp_tools.fitness_tool_3.get_coordinates", return_value=MOCK_COORDS), \
         patch("mcp_tools.fitness_tool_3.get_current_weather", return_value=MOCK_WEATHER_MILD):
        result = weather_adjusted_hydration_value(
            weight_kg=70, workout_minutes=60, city="Perth"
        )
    assert result["heat_adjustment_litres"] == 0.0
    assert result["humidity_adjustment_litres"] == 0.0
    assert result["adjusted_daily_target_litres"] == result["base_total_litres"]


def test_location_block_present():
    with patch("mcp_tools.fitness_tool_3.get_coordinates", return_value=MOCK_COORDS), \
         patch("mcp_tools.fitness_tool_3.get_current_weather", return_value=MOCK_WEATHER_MILD):
        result = weather_adjusted_hydration_value(
            weight_kg=80, workout_minutes=30, city="Perth"
        )
    assert result["location"]["resolved_city"] == "Perth"
    assert result["location"]["country"] == "Australia"
    assert result["location"]["input_city"] == "Perth"


def test_recommendation_contains_city():
    with patch("mcp_tools.fitness_tool_3.get_coordinates", return_value=MOCK_COORDS), \
         patch("mcp_tools.fitness_tool_3.get_current_weather", return_value=MOCK_WEATHER_MILD):
        result = weather_adjusted_hydration_value(
            weight_kg=70, workout_minutes=60, city="Perth"
        )
    assert "Perth" in result["recommendation"]
    assert "L" in result["recommendation"]
