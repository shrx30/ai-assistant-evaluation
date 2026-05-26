from tools.calculator_tool import (
    calculator_tool
)

from tools.time_tool import (
    time_tool
)

from tools.calculator_tool import (
    calculator_tool
)


TOOL_REGISTRY = {

    "calculator": {

        "handler": calculator_tool,

        "description":

            "Performs mathematical calculations.",

        "version": "1.0.0",

        "risk_level": "low",

        "retryable": False
    },

    "time": {

        "handler": time_tool,

        "description":

            "Returns current system time.",

        "version": "1.0.0",

        "risk_level": "low",

        "retryable": False
    }
}