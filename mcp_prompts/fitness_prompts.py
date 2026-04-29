"""MCP Prompts for the Personal Fitness Assistant."""

from __future__ import annotations
from typing import List, Dict


def hydration_planner_prompt(weight_kg: str, workout_minutes: str) -> List[Dict[str, str]]:
    """
    Dynamic prompt for daily hydration suggestions.
    Role: Sports Nutritionist.
    Uses: hydration_guide resource.

    Args:
        weight_kg: User's body weight in kilograms.
        workout_minutes: Duration of workout in minutes.

    Returns:
        Conversation template with role and user messages.
    """
    return [
        {
            "role": "system",
            "content": (
                "You are an experienced Sports Nutritionist. Using the hydration_guide resource which contains beverage hydration efficiency data, provide personalised daily hydration suggestions. Always recommend specific beverages from the guide and explain why they suit the user's needs."
            ),
        },
        {
            "role": "user",
            "content": (
                f"I weigh {weight_kg}kg and I worked out for {workout_minutes} minutes today. Based on the hydration guide, what beverages should I drink today and how much? Please give me a daily hydration plan."
            ),
        },
    ]


def sweat_analysis_prompt(workout_duration_min: str, intensity_level: str) -> List[Dict[str, str]]:
    """
    Dynamic prompt for post-workout mineral loss analysis.
    Role: Performance Nutritionist.
    Uses: electrolyte_directory resource.

    Args:
        workout_duration_min: Duration of workout in minutes.
        intensity_level: Intensity level - low, moderate, or high.

    Returns:
        Conversation template with role and user messages.
    """
    return [
        {
            "role": "system",
            "content": (
                "You are a Performance Nutritionist specialising in post-workout recovery.Using the electrolyte_directory resource which contains mineral loss data and recovery foods, explain what minerals the user has lost through sweat and suggest a  recovery meal."
            ),
        },
        {
            "role": "user",
            "content": (
                f"I just finished a {workout_duration_min} minute {intensity_level} intensity workout. Based on the electrolyte directory, what minerals did I lose through sweat and what recovery meal do you recommend to replenish them?"
            ),
        },
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
]