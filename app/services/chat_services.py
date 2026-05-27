from core.planner import create_plan

from models.oss_model import stream_response

from observability.logger import save_log

from observability.schemas import LogEvent

from guardrails.advanced_guardrails import (
    guardrail_check
)


def process_chat(user_input):

    # ---------------------------------
    # Guardrails
    # ---------------------------------

    guardrail_result = guardrail_check(
        user_input
    )

    if not guardrail_result["safe"]:

        return {

            "response": (
                guardrail_result["reason"]
            ),

            "plan": None
        }

    sanitized_prompt = (
        guardrail_result[
            "sanitized_prompt"
        ]
    )

    # ---------------------------------
    # Planner
    # ---------------------------------

    plan = create_plan(
        sanitized_prompt
    )

    # ---------------------------------
    # Messages
    # ---------------------------------

    messages = [

        {
            "role": "system",

            "content": (
                "You are a helpful AI assistant."
            )
        },

        {
            "role": "user",

            "content": sanitized_prompt
        }
    ]

    # ---------------------------------
    # Model Response
    # ---------------------------------

    response = stream_response(
        messages
    )

    # ---------------------------------
    # FIX STREAM / GENERATOR
    # ---------------------------------

    if not isinstance(response, str):

        try:

            response = "".join(

                chunk for chunk in response
            )

        except Exception:

            response = str(response)

    # ---------------------------------
    # Logging
    # ---------------------------------

    try:

        log_data = LogEvent(

            prompt=str(user_input),

            sanitized_prompt=str(
                sanitized_prompt
            ),

            response=str(response),

            plan=str(plan),

            safe=True
        )

        save_log(log_data)

    except Exception as e:

        print(
            f"Logging Error: {e}"
        )

    # ---------------------------------
    # Return
    # ---------------------------------

    return {

        "response": response,

        "plan": plan
    }