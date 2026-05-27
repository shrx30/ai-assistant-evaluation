from dataclasses import dataclass
from typing import Dict


@dataclass
class LogEvent:

    timestamp: str

    trace_id: str

    latency: float

    input: str

    response: str

    unsafe: bool

    plan: Dict

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
            self.plan,

            "observation":
            self.observation
        }