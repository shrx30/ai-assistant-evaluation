import time
import uuid

from datetime import datetime

from core.agent_loop import run_agent

from observability.logger import save_log

from memory.memory_manager import (
    add_message,
    get_history
)


def process_chat(user_input):

    trace_id = str(uuid.uuid4())

    add_message(
        "user",
        user_input
    )

    start_time = time.time()

    agent_result = run_agent(
        user_input
    )

    response = agent_result[
        "response"
    ]

    add_message(
        "assistant",
        response
    )

    plan = agent_result[
    "plan"
]

    print(
        "CURRENT MEMORY:"
    )

    print(
        get_history()
    )

    latency = round(
        time.time() - start_time,
        2
    )

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
          plan
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
