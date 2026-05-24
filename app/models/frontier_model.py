import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

def generate_response(prompt):

    completion = client.chat.completions.create(

        model="moonshotai/kimi-k2.6",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.3,
        top_p=0.95,
        max_tokens=60,
        stream=False
    )

    return completion.choices[0].message.content