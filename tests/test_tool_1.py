"""Tests for Tool 1 — Water Intake Calculator."""

from mcp_tools.fitness_tool_1 import calculate_water_intake_value


def test_basic_calculation():
    result = calculate_water_intake_value(weight_kg=70, workout_minutes=60)
    assert result["weight_kg"] == 70
    assert result["workout_minutes"] == 60
    # Base: 70 * 0.025 = 1.75, Exercise: 60/60 = 1.0, Total = 2.75
    assert result["total_daily_target_litres"] == 2.75


def test_no_workout():
    result = calculate_water_intake_value(weight_kg=60, workout_minutes=0)
    assert result["exercise_intake_litres"] == 0.0
    assert result["total_daily_target_litres"] == 60 * 0.025


def test_recommendation_string_present():
    result = calculate_water_intake_value(weight_kg=80, workout_minutes=30)
    assert "recommendation" in result
    assert "L" in result["recommendation"]
