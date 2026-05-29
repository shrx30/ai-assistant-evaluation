from models.oss_model import generate_response


def summarize_history(history):

    prompt = [
        {
            "role": "user",
            "content": (
                "Summarize this conversation into concise persistent memory:\n"
                + str(history)
            )
        }
    ]

    summary = generate_response(prompt)

    return summary if summary else ""