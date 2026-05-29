from dataclasses import dataclass

from datetime import datetime


@dataclass
class LogEvent:

    prompt: str

    sanitized_prompt: str

    response: str

    plan: str

    safe: bool

    timestamp: str = (
        datetime.utcnow().isoformat()
    )


    def to_dict(self):

        return {

            "prompt": str(
                self.prompt
            ),

            "sanitized_prompt": str(
                self.sanitized_prompt
            ),

            "response": str(
                self.response
            ),

            "plan": str(
                self.plan
            ),

            "safe": bool(
                self.safe
            ),

            "timestamp": str(
                self.timestamp
            )
        }
