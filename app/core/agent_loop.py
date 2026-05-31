from models.oss_model import (
    generate_response
)

from memory.memory_manager import (
    get_history
)

from core.planner import (
    create_plan
)

from tool.tool_router import (
    route_tool
)


def run_agent(user_input):

    plan = create_plan(
        user_input
    )

    tool_result = route_tool(
        user_input
    )

    print(
        "TOOL USED:",
        tool_result
    )

    if tool_result["tool"] == "calculator":

        return {

            "plan": plan,

            "observation": tool_result,

            "response": tool_result[
                "result"
            ]
        }

    history = get_history()

    if len(history) == 0:

        history = [

            {
                "role": "user",
                "content": user_input
            }
        ]

    response = generate_response(
        history
    )

    return {

        "plan": plan,

        "observation": "none",

        "response": response
    }
