import json


LOG_FILE = (
    "app/observability_logs.jsonl"
)


def save_log(data):

    try:

        with open(

            LOG_FILE,

            "a",

            encoding="utf-8"

        ) as file:

            file.write(

                json.dumps(

                    {

                        "timestamp":
                        str(data.timestamp),

                        "trace_id":
                        str(data.trace_id),

                        "latency":
                        float(data.latency),

                        "input":
                        str(data.input),

                        "response":
                        str(data.response),

                        "unsafe":
                        bool(data.unsafe),

                        "plan":
                        str(data.plan),

                        "observation":
                        str(data.observation)
                    }

                )

                + "\n"
            )

    except Exception as e:

        print(

            f"Logging Error: {str(e)}"
        )