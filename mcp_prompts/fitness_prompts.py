"""MCP Prompts for the Personal Fitness Assistant."""

from __future__ import annotations
from mcp.types import PromptMessage, TextContent, Message


def hydration_planner_prompt(weight_kg: str, workout_minutes: str) -> list[Message]:
    """
    Dynamic prompt for daily hydration suggestions.
    Role: Sports Nutritionist.
    Uses: hydration_guide resource.
    """
    return [
        Message(PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text=(
                    f"You are an experienced Sports Nutritionist. "
                    f"I weigh {weight_kg}kg and worked out for {workout_minutes} minutes today. "
                    f"Using the hydration guide beverage data, what should I drink today and how much? "
                    f"Give me a practical daily hydration plan with specific beverage recommendations."
                )
            )
        ))
    ]


def sweat_analysis_prompt(workout_duration_min: str, intensity_level: str) -> list[Message]:
    """
    Dynamic prompt for post-workout mineral loss analysis.
    Role: Performance Nutritionist.
    Uses: electrolyte_directory resource.
    """
    return [
        Message(PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text=(
                    f"You are a Performance Nutritionist specialising in post-workout recovery. "
                    f"I just finished a {workout_duration_min} minute {intensity_level} intensity workout. "
                    f"Based on the electrolyte directory mineral loss data, what minerals did I lose "
                    f"and what recovery meal do you recommend to replenish them?"
                )
            )
        ))
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