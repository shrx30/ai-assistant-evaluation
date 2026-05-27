from openai import OpenAI

import streamlit as st


client = OpenAI(

    base_url="https://integrate.api.nvidia.com/v1",

    api_key=st.secrets["NVIDIA_API_KEY"]
)


MODEL_NAME = "google/gemma-2-2b-it"

TEMPERATURE = 0.7

MAX_TOKENS = 120


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