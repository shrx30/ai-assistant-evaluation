import json
import re

from models.oss_model import (
    generate_response
)


TOOLS = """

Available tools:

1. calculator
Use ONLY for:
- arithmetic
- calculations
- math expressions

Examples:
- 2+2
- 25 * 18
- sqrt(144)

--------------------------------

2. time
Use ONLY for:
- current time requests

Examples:
- what time is it
- current time

"""


def plan_tool(user_input):

    planner_prompt = f"""

You are an AI tool planner.

Your task:
1. Decide if a tool is needed.
2. If needed, choose the correct tool.
3. Extract proper tool input.

IMPORTANT:
Return ONLY valid JSON.

JSON format:

{{
    "use_tool": true,
    "tool_name": "calculator",
    "tool_input": "25 * 18"
}}

OR

{{
    "use_tool": false
}}

{TOOLS}

Examples:

User:
hello

Output:
{{
    "use_tool": false
}}

--------------------------------

User:
how are you

Output:
{{
    "use_tool": false
}}

--------------------------------

User:
what is 25 * 18

Output:
{{
    "use_tool": true,
    "tool_name": "calculator",
    "tool_input": "25 * 18"
}}

--------------------------------

User:
what time is it

Output:
{{
    "use_tool": true,
    "tool_name": "time",
    "tool_input": "current time"
}}

--------------------------------

User request:
{user_input}

"""

    response = generate_response(

        [

            {

                "role": "user",

                "content": planner_prompt
            }
        ]
    )

    print("\nPLANNER RAW OUTPUT:")
    print(response)

    try:

        match = re.search(

            r"\{.*\}",

            response,

            re.DOTALL
        )

        if not match:

            return None

        json_text = match.group()

        print("\nEXTRACTED JSON:")
        print(json_text)

        plan = json.loads(
            json_text
        )

        # ---------------------------------
        # Explicit Tool Decision
        # ---------------------------------

        if not plan.get(
            "use_tool",
            False
        ):

            return None

        return plan

    except Exception as e:

        print("\nPLANNER ERROR:")
        print(str(e))

        return None