from models.oss_model import generate_response



def summarize_history(history):

    prompt = [

        {
            "role": "user",

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

    response_stream = generate_response(
        prompt
    )

    for chunk in response_stream:

        summary += chunk

    return summary