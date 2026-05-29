import json
import os


LOG_FILE = (
    "app/observability/observability_logs.jsonl"
)


def save_log(data):

    try:

        print(
            "SAVE_LOG CALLED"
        )

        print(
            data
        )

        os.makedirs(
            os.path.dirname(LOG_FILE),
            exist_ok=True
        )

        with open(
            LOG_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(

                json.dumps(
                    data,
                    default=str
                )

                + "\n"
            )

        print(
            "LOG WRITTEN TO:",
            LOG_FILE
        )

    except Exception as e:

        print(
            "LOGGING ERROR:",
            str(e)
        )
