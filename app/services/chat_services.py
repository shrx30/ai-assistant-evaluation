import time
import uuid

from datetime import datetime

from memory.memory_manager import (
    add_message,
    get_history
)

from observability.logger import (
    save_log
)

from core.config import (
    BLOCKED_WORDS
)

from core.agent_loop import (
    run_agent
)


def process_chat(user_input):

    trace_id = str(uuid.uuid4())

    add_message(
        "user",
        user_input
    )

    history = get_history()

    unsafe = any(

        word in user_input.lower()

        for word in BLOCKED_WORDS
    )

    start_time = time.time()


    # --------------------------------
    # GUARDRAILS
    # --------------------------------

    if unsafe:

        response = (
            "Unsafe request blocked."
        )

        plan = {
            "tool": "none"
        }

        observation = (
            "Blocked by guardrails."
        )

    else:

        # ----------------------------
        # AGENT EXECUTION
        # ----------------------------

        agent_result = run_agent(
            user_input
        )

        plan = agent_result[
            "plan"
        ]

        observation = agent_result[
            "observation"
        ]

        response_stream = agent_result[
            "response_stream"
        ]


        # ----------------------------
        # CONSUME STREAM
        # ----------------------------

        response = ""

        for chunk in response_stream:

            response += chunk


    end_time = time.time()

    latency = round(
        end_time - start_time,
        2
    )


    # --------------------------------
    # OBSERVABILITY LOGS
    # --------------------------------

    log_data = {

        "timestamp": datetime.now().isoformat(),

        "trace_id": trace_id,

        "latency": latency,

        "input": user_input,

        "response": response,

        "unsafe": unsafe,

        "plan": str(plan),

        "observation": observation
    }

    save_log(log_data)


    # --------------------------------
    # SAVE MEMORY
    # --------------------------------

    add_message(
        "assistant",
        response
    )


    # --------------------------------
    # RETURN
    # --------------------------------

    return {

        "response": response,

        "latency": latency,

        "trace_id": trace_id,

        "unsafe": unsafe
    }