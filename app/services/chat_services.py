import time
import uuid

from datetime import datetime

from core.agent_loop import run_agent

from observability.logger import save_log

from memory.memory_manager import (
    add_message,
    get_history
)

from guardrails.guardrails import (
    is_safe
)


def process_chat(user_input):

    trace_id = str(uuid.uuid4())

    # -------------------------
    # GUARDRAILS
    # -------------------------

    safe_request = is_safe(
        user_input
    )

    if not safe_request:

        save_log({

            "timestamp":
            datetime.now().isoformat(),

            "trace_id":
            trace_id,

            "input":
            user_input,

            "response":
            "Blocked by guardrails",

            "safe_request":
            False
        })

        return {

            "response":
            "Request blocked by guardrails.",

            "latency":
            0,

            "trace_id":
            trace_id,

            "unsafe":
            True
        }

    # -------------------------
    # MEMORY
    # -------------------------

    add_message(
        "user",
        user_input
    )

    start_time = time.time()

    # -------------------------
    # AGENT
    # -------------------------

    agent_result = run_agent(
        user_input
    )

    response = agent_result[
        "response"
    ]

    plan = agent_result[
        "plan"
    ]

    observation = agent_result[
        "observation"
    ]

    add_message(
        "assistant",
        response
    )

    latency = round(
        time.time() - start_time,
        2
    )

    # -------------------------
    # OBSERVABILITY
    # -------------------------

    save_log({

        "timestamp":
        datetime.now().isoformat(),

        "trace_id":
        trace_id,

        "latency":
        latency,

        "input":
        user_input,

        "response":
        response,

        "plan":
        plan,

        "observation":
        observation,

        "safe_request":
        True
    })

    return {

        "response":
        response,

        "latency":
        latency,

        "trace_id":
        trace_id,

        "unsafe":
        False
    }
