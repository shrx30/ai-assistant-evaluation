from tools.calculator import (
    calculate
)


def route_tool(user_input):

    math_chars = [
        "+",
        "-",
        "*",
        "/"
    ]

    if any(
        char in user_input
        for char in math_chars
    ):

        result = calculate(
            user_input
        )

        if result is not None:

            return {

                "tool": "calculator",

                "result": result
            }

    return {

        "tool": None,

        "result": None
    }
