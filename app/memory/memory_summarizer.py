from app.models.oss_model import (
    stream_response
)


def summarize_history(history):

    prompt = [

        {
            "role": "system",

            "content":

            (
                "Summarize the conversation "
                "into concise persistent memory."
            )
        },

        {
            "role": "user",

            "content": str(history)
        }
    ]


    summary = ""

    response_stream = stream_response(
        prompt
    )

    for chunk in response_stream:

        summary += chunk

    return summary