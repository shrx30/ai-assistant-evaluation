import json

from dataclasses import (
    dataclass
)


def make_serializable(obj):

    try:

        json.dumps(obj)

        return obj

    except Exception:

        if isinstance(obj, dict):

            return {

                str(k):
                make_serializable(v)

                for k, v in obj.items()
            }

        elif isinstance(obj, list):

            return [

                make_serializable(x)

                for x in obj
            ]

        else:

            return str(obj)


@dataclass
class LogEvent:

    timestamp: str

    trace_id: str

    latency: float

    input: str

    response: str

    unsafe: bool

    plan: object

    observation: str


    def to_dict(self):

        return {

            "timestamp":
            self.timestamp,

            "trace_id":
            self.trace_id,

            "latency":
            self.latency,

            "input":
            self.input,

            "response":
            self.response,

            "unsafe":
            self.unsafe,

            "plan":
            make_serializable(
                self.plan
            ),

            "observation":
            self.observation
        }