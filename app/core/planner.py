import json

from models.oss_model import (
    stream_response
)


def create_plan(user_input):

    planning_prompt = [

        {
            "role": "system",

            "content":

            (
                "You are an AI planner.\n\n"

                "Return ONLY valid JSON.\n\n"

                "Available tools:\n"

                "1. calculator\n"
                "2. time\n\n"

                "Example:\n"

                '{'
                '"tool": "calculator", '
                '"input": "25 * 4"'
                '}\n\n'

                "If no tool needed:\n"

                '{'
                '"tool": "none", '
                '"input": ""'
                '}'
            )
        },

        {
            "role": "user",

            "content": user_input
        }
    ]


    response_stream = stream_response(
        planning_prompt
    )

    full_response = ""

    for chunk in response_stream:

        full_response += chunk


    try:

        return json.loads(
            full_response
        )

    except Exception:

        return {

            "tool": "none",

            "input": ""
        }