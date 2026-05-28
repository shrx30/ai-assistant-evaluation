import json


LOG_FILE = (
    "app/observability_logs.jsonl"
)


def save_log(log_event):

    try:

        serialized = json.dumps(

            log_event.to_dict(),

            default=lambda o: str(o)
        )

    except Exception as e:

        serialized = json.dumps({

            "logging_error": str(e)
        })

    with open(

        LOG_FILE,

        "a",

        encoding="utf-8"

    ) as file:

        file.write(
            serialized + "\n"
        )