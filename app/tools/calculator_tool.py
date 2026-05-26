import time

from tools.schemas import (

    CalculatorInput,

    ToolResponse
)


TOOL_VERSION = "1.0.0"


def calculator_tool(

    tool_input,

    trace_id
):

    start = time.time()

    try:

        validated = CalculatorInput(

            expression=tool_input
        )

        result = eval(

            validated.expression
        )

        latency = round(

            (time.time() - start)

            * 1000,

            2
        )

        return ToolResponse(

            status="ok",

            tool_name="calculator",

            tool_version=TOOL_VERSION,

            trace_id=trace_id,

            latency_ms=latency,

            data={

                "result": result
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

            tool_name="calculator",

            tool_version=TOOL_VERSION,

            trace_id=trace_id,

            latency_ms=latency,

            error_code="VALIDATION",

            error_message=str(e)
        ).dict()