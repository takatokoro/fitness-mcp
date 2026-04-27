"""MCP Resources for the Personal Fitness Assistant."""

from __future__ import annotations
from typing import Any, Dict


def hydration_guide() -> Dict[str, Any]:
    """
    A dataset of beverages and their hydration efficiency.
    Used by the hydration_planner prompt.
    """
    return {
        "id": "hydration-guide",
        "title": "Beverage Hydration Efficiency Guide",
        "beverages": [
            {
                "name": "Water",
                "hydration_score": 1.0,
                "notes": "Best all-round hydration source"
            },
            {
                "name": "Coconut Water",
                "hydration_score": 0.95,
                "notes": "Natural electrolytes, good post-workout"
            },
            {
                "name": "Sports Drink (e.g. Gatorade)",
                "hydration_score": 0.90,
                "notes": "Contains sodium and sugar, good for long sessions"
            },
            {
                "name": "Milk",
                "hydration_score": 0.85,
                "notes": "High in electrolytes, good recovery drink"
            },
            {
                "name": "Orange Juice",
                "hydration_score": 0.75,
                "notes": "High sugar content, moderate hydration"
            },
            {
                "name": "Coffee",
                "hydration_score": 0.50,
                "notes": "Mild diuretic, not ideal for hydration"
            },
            {
                "name": "Soft Drink",
                "hydration_score": 0.30,
                "notes": "High sugar, low hydration value"
            }
        ],
        "notes": "Hydration score is relative to water (1.0 = most hydrating)"
    }


def electrolyte_directory() -> Dict[str, Any]:
    """
    Reference guide on mineral loss through sweat and recovery food sources.
    Used by the sweat_analysis prompt.
    """
    return {
        "id": "electrolyte-directory",
        "title": "Electrolyte Loss and Recovery Directory",
        "minerals": [
            {
                "name": "Sodium",
                "lost_per_litre_sweat_mg": 900,
                "role": "Fluid balance and nerve function",
                "recovery_foods": ["Salted nuts", "Pretzels", "Pickle juice", "Table salt"]
            },
            {
                "name": "Potassium",
                "lost_per_litre_sweat_mg": 200,
                "role": "Muscle contraction and heart function",
                "recovery_foods": ["Banana", "Sweet potato", "Avocado", "Spinach"]
            },
            {
                "name": "Magnesium",
                "lost_per_litre_sweat_mg": 36,
                "role": "Muscle recovery and energy production",
                "recovery_foods": ["Dark chocolate", "Almonds", "Pumpkin seeds", "Brown rice"]
            }
        ]
    }


RESOURCE_DEFINITIONS = [
    {
        "name": "hydration_guide",
        "description": "A dataset of beverages and their hydration efficiency scores.",
        "mime_type": "application/json",
        "func": hydration_guide,
    },
    {
        "name": "electrolyte_directory",
        "description": "Mineral loss data through sweat and recommended recovery foods.",
        "mime_type": "application/json",
        "func": electrolyte_directory,
    },
]