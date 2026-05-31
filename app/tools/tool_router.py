import re

from tools.calculator import (
    calculate
)


def route_tool(user_input):

    expression = re.sub(
        r"[^0-9+\-*/(). ]",
        "",
        user_input
    ).strip()

    if expression:

        result = calculate(
            expression
        )

        if result is not None:

            return {

                "tool":
                "calculator",

                "result":
                result
            }

    return {

        "tool":
        None,

        "result":
        None
    }
