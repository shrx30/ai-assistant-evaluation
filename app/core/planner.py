import json

from models.oss_model import (
    generate_response
)


def create_plan(user_input):

    planning_prompt = [

        {
            "role": "user",

            "content": (
                "You are an AI planner.\n\n"
                "Return ONLY valid JSON.\n\n"
                "Available tools:\n"
                "1. calculator\n"
                "2. time\n\n"
                "Example:\n"
                '{"tool": "calculator", "input": "25 * 4"}\n\n'
                "If no tool needed:\n"
                '{"tool": "none", "input": ""}'
            )
        },

        {
            "role": "user",
            "content": user_input
        }
    ]

    full_response = generate_response(planning_prompt)

    try:

        return json.loads(full_response)

    except Exception:

        return {
            "tool": "none",
            "input": ""
        }