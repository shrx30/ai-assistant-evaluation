import time
import uuid

from datetime import datetime

from core.agent_loop import (
    run_agent
)


def process_chat(user_input):

    trace_id = str(uuid.uuid4())

    start_time = time.time()

    agent_result = run_agent(
        user_input
    )

    response = agent_result[
        "response"
    ]

    latency = round(
        time.time() - start_time,
        2
    )

    return {

        "response": response,

        "latency": latency,

        "trace_id": trace_id,

        "unsafe": False
    }
