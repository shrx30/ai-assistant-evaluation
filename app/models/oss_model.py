import os

from openai import OpenAI


MODEL_NAME = "google/gemma-2-2b-it"


client = OpenAI(

    base_url="https://integrate.api.nvidia.com/v1",

    api_key=os.getenv("NVIDIA_API_KEY")
)


# ----------------------------------------
# Generate response
# ----------------------------------------

def generate_response(messages):

    try:

        completion = client.chat.completions.create(

            model=MODEL_NAME,

            messages=messages,

            temperature=0.7,

            top_p=0.7,

            max_tokens=256,

            stream=True
        )

        full_response = ""

        for chunk in completion:

            if (

                chunk.choices

                and chunk.choices[0].delta.content
                is not None
            ):

                content = chunk.choices[
                    0
                ].delta.content

                full_response += content

        return full_response.strip()

    except Exception as e:

        return f"Inference Error: {str(e)}"