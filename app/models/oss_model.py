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


def stream_response(messages):

    try:

        completion = client.chat.completions.create(

            model=MODEL_NAME,

            messages=messages,

            temperature=TEMPERATURE,

            top_p=0.7,

            max_tokens=MAX_TOKENS,

            stream=True
        )

        for chunk in completion:

            if (

                chunk.choices

                and chunk.choices[0].delta.content
                is not None
            ):

                yield chunk.choices[
                    0
                ].delta.content

    except Exception as e:

        yield f"Inference Error: {str(e)}"