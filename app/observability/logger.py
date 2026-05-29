import json
import os


LOG_FILE = (
    "app/observability/observability_logs.jsonl"
)


def save_log(data):

    try:

        os.makedirs(
            os.path.dirname(LOG_FILE),
            exist_ok=True
        )


        print("LOG FILE:", LOG_FILE)
        print("LOG DATA:", data)

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

    except Exception as e:

        print(

            f"Logging Error: {str(e)}"
        )
