from app.tools.tool_registry import (
    TOOL_REGISTRY
)


def execute_tool(user_input):

    lowered = user_input.lower()


    if "time" in lowered:

        return TOOL_REGISTRY[
            "time"
        ](user_input)


    if any(

        char.isdigit()

        for char in user_input
    ):

        cleaned = (

            user_input

            .replace("calculate", "")

            .replace("what is", "")

            .strip()
        )

        return TOOL_REGISTRY[
            "calculator"
        ](cleaned)


    return None