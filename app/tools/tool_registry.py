from app.tools.calculator_tool import (
    calculator_tool
)

from app.tools.time_tool import (
    time_tool
)


TOOL_REGISTRY = {

    "calculator": calculator_tool,

    "time": time_tool
}