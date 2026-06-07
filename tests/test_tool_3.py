"""Tests for Tool 3 — Weather-Adjusted Hydration (Open-Meteo mocked)."""

from unittest.mock import patch
from mcp_tools.fitness_tool_3 import weather_adjusted_hydration_value

# Fake weather response — replaces the real Open-Meteo call in all tests below
MOCK_WEATHER_HOT = {
    "temperature_celsius": 35.0,   # 10 degrees above 25 → +1.0L heat adjustment
    "relative_humidity_percent": 80,  # above 60% → +0.2L humidity adjustment
    "source": "Open-Meteo",
}

MOCK_WEATHER_MILD = {
    "temperature_celsius": 20.0,   # below 25 → no heat adjustment
    "relative_humidity_percent": 40,  # below 60% → no humidity adjustment
    "source": "Open-Meteo",
}


def test_hot_weather_increases_target():
    with patch("mcp_tools.fitness_tool_3.get_current_weather", return_value=MOCK_WEATHER_HOT):
        result = weather_adjusted_hydration_value(
            weight_kg=70, workout_minutes=60, latitude=-31.95, longitude=115.86
        )
    # Base total: (70*0.025) + (60/60) = 1.75 + 1.0 = 2.75
    # Heat adj: (35-25)*0.1 = 1.0
    # Humidity adj: 0.2
    # Adjusted: 2.75 + 1.0 + 0.2 = 3.95
    assert result["adjusted_daily_target_litres"] == 3.95
    assert result["heat_adjustment_litres"] == 1.0
    assert result["humidity_adjustment_litres"] == 0.2


def test_mild_weather_no_adjustment():
    with patch("mcp_tools.fitness_tool_3.get_current_weather", return_value=MOCK_WEATHER_MILD):
        result = weather_adjusted_hydration_value(
            weight_kg=70, workout_minutes=60, latitude=-31.95, longitude=115.86
        )
    assert result["heat_adjustment_litres"] == 0.0
    assert result["humidity_adjustment_litres"] == 0.0
    assert result["adjusted_daily_target_litres"] == result["base_total_litres"]


def test_recommendation_string_present():
    with patch("mcp_tools.fitness_tool_3.get_current_weather", return_value=MOCK_WEATHER_MILD):
        result = weather_adjusted_hydration_value(
            weight_kg=80, workout_minutes=30, latitude=0, longitude=0
        )
    assert "recommendation" in result
    assert "L" in result["recommendation"]
