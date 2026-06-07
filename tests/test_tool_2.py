"""Tests for Tool 2 v1 — Sweat Loss Estimator (CSV)."""

import pytest
from mcp_tools.fitness_tool_2_v1 import estimate_sweat_loss_value


def test_low_intensity():
    result = estimate_sweat_loss_value(workout_duration_min=60, intensity_level="low")
    assert result["intensity_level"] == "low"
    assert result["fluid_lost_litres"] > 0


def test_high_intensity():
    result = estimate_sweat_loss_value(workout_duration_min=60, intensity_level="high")
    assert result["fluid_lost_litres"] > 0
    assert result["sodium_lost_mg"] > 0


def test_invalid_intensity_raises():
    with pytest.raises(ValueError):
        estimate_sweat_loss_value(workout_duration_min=60, intensity_level="extreme")


def test_recommended_replacement_is_higher_than_lost():
    result = estimate_sweat_loss_value(workout_duration_min=90, intensity_level="moderate")
    assert result["recommended_replacement_litres"] > result["fluid_lost_litres"]
