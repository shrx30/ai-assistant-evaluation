import time
import uuid

from datetime import datetime

from models.oss_model import (
    generate_response
)

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

    if unsafe:

        response = (
            "Unsafe request blocked."
        )

    else:

        response = generate_response(
            history
        )

    end_time = time.time()

    latency = round(
        end_time - start_time,
        2
    )

    log_data = {

        "timestamp": datetime.now().isoformat(),

        "trace_id": trace_id,

        "latency": latency,

        "input": user_input,

        "response": response,

        "unsafe": unsafe
    }

    save_log(log_data)

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