import json

from datetime import datetime


LOG_FILE = "app/observability_logs.jsonl"


def save_log(data):

    with open(

        LOG_FILE,

        "a",

        encoding="utf-8"

    ) as file:

        file.write(

            json.dumps(data)

            + "\n"
        )