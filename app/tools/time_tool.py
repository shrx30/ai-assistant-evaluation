import time

from datetime import datetime

from tools.schemas import (
    ToolResponse
)


TOOL_VERSION = "1.0.0"


def time_tool(

    tool_input,

    trace_id
):

    start = time.time()

    try:

        current_time = datetime.now().strftime(
            "%H:%M:%S"
        )

        latency = round(

            (time.time() - start)

            * 1000,

            2
        )

        return ToolResponse(

            status="ok",

            tool_name="time",

            tool_version=TOOL_VERSION,

            trace_id=trace_id,

            latency_ms=latency,

            data={

                "current_time": current_time
            }

        ).dict()

    except Exception as e:

        latency = round(

            (time.time() - start)

            * 1000,

            2
        )

        return ToolResponse(

            status="error",

            tool_name="time",

            tool_version=TOOL_VERSION,

            trace_id=trace_id,

            latency_ms=latency,

            error_code="UNKNOWN",

            error_message=str(e)

        ).dict()