"""MCP Prompts for the Personal Fitness Assistant."""

from __future__ import annotations
from fastmcp.prompts import Message


def hydration_planner_prompt(weight_kg: str, workout_minutes: str) -> list[Message]:
    """
    Dynamic prompt for daily hydration suggestions.
    Role: Sports Nutritionist.
    Uses: hydration_guide resource.
    """
    return [
        Message(
            role="user",
            content=(
                f"You are an experienced Sports Nutritionist. "
                f"I weigh {weight_kg}kg and worked out for {workout_minutes} minutes today. "
                f"Using the hydration guide beverage data, what should I drink today and how much? "
                f"Give me a practical daily hydration plan with specific beverage recommendations."
            )
        )
    ]


def sweat_analysis_prompt(workout_duration_min: str, intensity_level: str) -> list[Message]:
    """
    Dynamic prompt for post-workout mineral loss analysis.
    Role: Performance Nutritionist.
    Uses: electrolyte_directory resource.
    """
    return [
        Message(
            role="user",
            content=(
                f"You are a Performance Nutritionist specialising in post-workout recovery. "
                f"I just finished a {workout_duration_min} minute {intensity_level} intensity workout. "
                f"Based on the electrolyte directory mineral loss data, what minerals did I lose "
                f"and what recovery meal do you recommend to replenish them?"
            )
        )
    ]


def ai_fitness_summary_prompt(
    weight_kg: str,
    workout_minutes: str,
    city: str,
    intensity_level: str,
) -> list[Message]:
    """
    Prompt 3 — AI Fitness Coaching Summary.

    Instructs the AI to act as a fitness coach and produce a plain English
    summary combining hydration, sweat loss and weather data.
    The AI client (e.g. Claude Desktop) will call Tool 1, Tool 2 and Tool 3
    to gather the data, then use this prompt to synthesise a coaching response.

    Role: Friendly sports nutrition coach.
    Uses: Tool 1, Tool 2 v1, Tool 3 results + weather_context resource.
    """
    return [
        Message(
            role="user",
            content=(
                f"You are a friendly sports nutrition coach. "
                f"I weigh {weight_kg}kg and just finished a {workout_minutes} minute "
                f"{intensity_level} intensity workout in {city}. "
                f"Please: "
                f"1. Call the calculate_water_intake tool with weight_kg={weight_kg} and workout_minutes={workout_minutes}. "
                f"2. Call the estimate_sweat_loss tool with workout_duration_min={workout_minutes} and intensity_level={intensity_level}. "
                f"3. Call the weather_adjusted_hydration tool with weight_kg={weight_kg}, workout_minutes={workout_minutes} and city={city}. "
                f"4. Read the weather_context resource for current conditions. "
                f"Then give me a short, friendly coaching summary (3-4 sentences) covering "
                f"how much to drink, what minerals I lost, what to eat to recover, "
                f"and any weather-specific advice for today in {city}."
            )
        )
    ]


PROMPT_DEFINITIONS = [
    {
        "name": "hydration_planner",
        "description": "Sports Nutritionist providing personalised daily hydration suggestions.",
        "func": hydration_planner_prompt,
    },
    {
        "name": "sweat_analysis",
        "description": "Performance Nutritionist explaining mineral loss and suggesting recovery meals.",
        "func": sweat_analysis_prompt,
    },
    {
        "name": "ai_fitness_summary",
        "description": (
            "Friendly fitness coach that combines all tool results and weather data "
            "into a plain English coaching summary. Calls Tool 1, Tool 2 and Tool 3 "
            "automatically then synthesises the results."
        ),
        "func": ai_fitness_summary_prompt,
    },
]
