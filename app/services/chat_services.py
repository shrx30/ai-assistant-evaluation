import time
import uuid

from datetime import datetime

from core.agent_loop import run_agent

from observability.logger import save_log


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

   print("BEFORE SAVE_LOG")

save_log({
    "timestamp": datetime.now().isoformat(),
    "trace_id": trace_id,
    "latency": latency,
    "input": user_input,
    "response": response
})

print("AFTER SAVE_LOG")

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
