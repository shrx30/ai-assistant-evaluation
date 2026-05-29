from core.planner import (
    create_plan
)

from tools.tool_registry import (
    TOOL_REGISTRY
)

from models.oss_model import (
    generate_response
)


def run_agent(user_input):

    plan = create_plan(
        user_input
    )

    tool_name = plan.get(
        "tool",
        "none"
    )

    tool_input = plan.get(
        "input",
        ""
    )


    # --------------------------------
    # TOOL EXECUTION
    # --------------------------------

    if (

        tool_name != "none"

        and tool_name in TOOL_REGISTRY
    ):

        tool_result = TOOL_REGISTRY[
            tool_name
        ](tool_input)

        observation = (

            f"Tool Used: {tool_name}\n"

            f"Tool Result: {tool_result}"
        )

    else:

        observation = (
            "No tool used."
        )


    # --------------------------------
    # FINAL RESPONSE
    # --------------------------------

    final_prompt = [

    {
        "role": "user",

        "content":

        (
            "You are an AI agent.\n\n"

            "Use observations carefully.\n\n"

            f"User Input:\n{user_input}\n\n"

            f"Plan:\n{plan}\n\n"

            f"Observation:\n{observation}"
        )
    }
]


    response = generate_response(
        final_prompt
    )

    return {

        "plan": plan,

        "observation": observation,

        "response": response
    }