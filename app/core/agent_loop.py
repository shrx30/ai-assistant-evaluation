from models.oss_model import (
    generate_response
)

from memory.memory_manager import (
    get_history
)


def run_agent(user_input):

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

        "plan": "disabled",

        "observation": "disabled",

        "response": response
    }
