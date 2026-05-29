from models.oss_model import (
    generate_response
)


def run_agent(user_input):

    response = generate_response(

        [
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    return {

        "plan": "disabled",

        "observation": "disabled",

        "response": response
    }
