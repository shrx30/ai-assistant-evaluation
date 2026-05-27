import time
import uuid

from datetime import datetime

from app.core.planner import (
    create_plan
)
from app.models.oss_model import (
    stream_response
)
from app.memory.memory_manager import (
    add_message,
    get_history
)

from app.observability.logger import (
    save_log
)

from app.core.config import (
    BLOCKED_WORDS
)

from app.tools.tool_router import (
    execute_tool
)

from app.core.planner import (
    create_plan
)
from app.core.agent_loop import (
    run_agent
)

def process_chat(user_input):

    trace_id = str(uuid.uuid4())

    plan = create_plan(
    user_input
       )

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
    # Guardrails
    # --------------------------------

    if unsafe:

        response = (
            "Unsafe request blocked."
        )

    else:

        # ----------------------------
        # Tool Execution
        # ----------------------------
        plan = create_plan(
        user_input
          )  
        


        agent_result = run_agent(
    user_input
)

        plan = agent_result[
    "plan"
]

        observation = agent_result[
    "observation"
]

        response = agent_result[
    "response_stream"
]


    end_time = time.time()

    latency = round(
        end_time - start_time,
        2
    )


    # --------------------------------
    # Observability Logs
    # --------------------------------

    log_data = {

        "timestamp": datetime.now().isoformat(),

        "trace_id": trace_id,

        "latency": latency,

        "input": user_input,

        "response": response,

        "unsafe": unsafe,

        "plan": plan,


        

        "observation": observation,
    }

    save_log(log_data)


    # --------------------------------
    # Save Assistant Response
    # --------------------------------

    add_message(
        "assistant",
        response
    )


    return {

        "response": response,

        "latency": latency,

        "trace_id": trace_id,

        "unsafe": unsafe
    }