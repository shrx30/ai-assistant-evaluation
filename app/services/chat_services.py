import time
import uuid

from core.planner import create_plan
from models.oss_model import generate_response
from guardrails.advanced_guardrails import guardrail_check
from observability.logger import save_log
from observability.schemas1 import LogEvent


def process_chat(user_input):

    trace_id = str(uuid.uuid4())
    start_time = time.time()

    # ---------------------------------
    # Guardrails
    # ---------------------------------

    guardrail_result = guardrail_check(user_input)

    if not guardrail_result["safe"]:
        latency = round(time.time() - start_time, 3)
        return {
            "response": guardrail_result["reason"],
            "plan": None,
            "latency": latency,
            "trace_id": trace_id,
            "unsafe": True
        }

    sanitized_prompt = guardrail_result["sanitized_prompt"]

    # ---------------------------------
    # Planner
    # ---------------------------------

    try:
        plan = create_plan(sanitized_prompt)
        if not isinstance(plan, str):
            plan = str(plan)
    except Exception as e:
        plan = f"Planner Error: {str(e)}"

    # ---------------------------------
    # Messages
    # ---------------------------------

    messages = [
        {
            "role": "user",
            "content": "You are a helpful AI assistant."
        },
        {
            "role": "user",
            "content": sanitized_prompt
        }
    ]

    # ---------------------------------
    # Generate Response
    # ---------------------------------

    try:
        response = generate_response(messages)

        if hasattr(response, "__iter__") and not isinstance(response, str):
            try:
                response = "".join(list(response))
            except Exception:
                response = str(response)
        else:
            response = str(response)

    except Exception as e:
        response = f"Inference Error: {str(e)}"

    # ---------------------------------
    # Latency
    # ---------------------------------

    latency = round(time.time() - start_time, 3)

    # ---------------------------------
    # Logging
    # ---------------------------------

    try:
        log_data = LogEvent(
            prompt=str(user_input),
            sanitized_prompt=str(sanitized_prompt),
            response=str(response),
            plan=str(plan),
            safe=True
        )
        save_log(log_data)

    except Exception as e:
        print(f"Logging Error: {str(e)}")

    # ---------------------------------
    # Return
    # ---------------------------------

    return {
        "response": response,
        "plan": plan,
        "latency": latency,
        "trace_id": trace_id,
        "unsafe": False
    }