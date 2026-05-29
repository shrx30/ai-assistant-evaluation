import time
import uuid

from datetime import datetime

from core.agent_loop import run_agent

from observability.logger import save_log

from observability.schemas import LogEvent


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
        False,

        plan=
        "disabled",

        observation=
        "disabled"
    )

    save_log(
        log_event
    )

    return {

        "response": response,

        "latency": latency,

        "trace_id": trace_id,

        "unsafe": False
    }
