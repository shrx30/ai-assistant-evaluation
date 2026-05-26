from tools.tool_registry import (
    TOOL_REGISTRY
)


def execute_tool(

    tool_name,

    tool_input,

    trace_id
):

    tool_meta = TOOL_REGISTRY.get(
        tool_name
    )

    if not tool_meta:

        return None

    handler = tool_meta["handler"]

    return handler(

        tool_input,

        trace_id
    )