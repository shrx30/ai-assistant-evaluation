import os

from openai import OpenAI

from app.core.config import (
    MODEL_NAME,
    TEMPERATURE,
    MAX_TOKENS
)


client = OpenAI(

    base_url="https://integrate.api.nvidia.com/v1",

    api_key=os.getenv("NVIDIA_API_KEY")
)


def generate_response(messages):

    try:

        completion = client.chat.completions.create(

            model=MODEL_NAME,

            messages=messages,

            temperature=TEMPERATURE,

            top_p=0.7,

            max_tokens=MAX_TOKENS,

            stream=False
        )

        response = completion.choices[
            0
        ].message.content

        return response

    except Exception as e:

        return f"Inference Error: {str(e)}"