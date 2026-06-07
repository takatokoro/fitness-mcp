from .fitness_tool_1 import router as water_intake_router, TOOL_DEFINITIONS as WATER_TOOL_DEFINITIONS
from .fitness_tool_2_v1 import router as sweat_loss_router, TOOL_DEFINITIONS as SWEAT_V1_TOOL_DEFINITIONS
from .fitness_tool_2_v2 import router as sweat_loss_v2_router, TOOL_DEFINITIONS as SWEAT_V2_TOOL_DEFINITIONS
from .fitness_tool_3 import router as weather_hydration_router, TOOL_DEFINITIONS as WEATHER_TOOL_DEFINITIONS

TOOL_DEFINITIONS = (
    WATER_TOOL_DEFINITIONS
    + SWEAT_V1_TOOL_DEFINITIONS
    + SWEAT_V2_TOOL_DEFINITIONS
    + WEATHER_TOOL_DEFINITIONS
)
