import json


LOG_FILE = (
    "app/observability_logs.jsonl"
)


def save_log(log_event):

    with open(

        LOG_FILE,

        "a",

        encoding="utf-8"

    ) as file:

        file.write(

            json.dumps(

                log_event.to_dict(),

                default=str
            )

            + "\n"
        )