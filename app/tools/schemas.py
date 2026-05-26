from pydantic import BaseModel

from pydantic import Field

from typing import Optional

from typing import Literal


# ---------------------------------
# Calculator Input
# ---------------------------------

class CalculatorInput(BaseModel):

    expression: str = Field(

        min_length=1,

        max_length=100
    )


# ---------------------------------
# Standard Tool Output
# ---------------------------------

class ToolResponse(BaseModel):

    status: Literal[

        "ok",

        "error"
    ]

    tool_name: str

    tool_version: str

    trace_id: str

    latency_ms: float

    data: Optional[dict] = None

    error_code: Optional[str] = None

    error_message: Optional[str] = None