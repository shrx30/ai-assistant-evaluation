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

from observability.schemas import (
    LogEvent
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

        plan = "none"

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

        plan = str(

            agent_result["plan"]
        )

        observation = agent_result[
            "observation"
        ]

        response = agent_result[
            "response"
        ]


    end_time = time.time()

    latency = round(
        end_time - start_time,
        2
    )


    # --------------------------------
    # OBSERVABILITY
    # --------------------------------

    log_event = LogEvent(

        timestamp=
        datetime.now().isoformat(),

        trace_id=
        trace_id,

        latency=
        latency,

        input=
        user_input,

        response=
        response,

        unsafe=
        unsafe,

        plan=
        plan,

        observation=
        observation
    )

    save_log(log_event)


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