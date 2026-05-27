import json


LOG_FILE = (
    "app/observability_logs.jsonl"
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


def save_log(data):

    try:

        serializable_data = (
            make_serializable(data)
        )

        with open(

            LOG_FILE,

            "a",

            encoding="utf-8"

        ) as file:

            file.write(

                json.dumps(
                    serializable_data
                )

                + "\n"
            )

    except Exception as e:

        print(

            f"Logging Error: {str(e)}"
        )