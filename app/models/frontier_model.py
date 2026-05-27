import os
import requests

from telemetry import tracer


MODEL_NAME = "google/gemma-2-2b-it"

API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

HEADERS = {

    "Authorization": f"Bearer {os.getenv('NVIDIA_API_KEY')}",

    "Content-Type": "application/json"
}


# ----------------------------------------
# Generate response
# ----------------------------------------

def generate_response(messages):

    print("\n[OBSERVABILITY] Starting inference...\n")

    print("GENERATE_RESPONSE FUNCTION CALLED")


    with tracer.start_as_current_span(
        "nvidia_gemma_inference"
    ) as span:

        span.set_attribute(
            "model.name",
            MODEL_NAME
        )

        span.set_attribute(
            "conversation.length",
            len(messages)
        )

        payload = {

            "model": MODEL_NAME,

            "messages": messages,

            "temperature": 0.7,

            "max_tokens": 120
        }

        try:

            response = requests.post(

                API_URL,

                headers=HEADERS,

                json=payload,

                timeout=60
            )

            result = response.json()

            assistant_reply = result[
                "choices"
            ][0][
                "message"
            ][
                "content"
            ]

            span.set_attribute(
                "response.length",
                len(assistant_reply)
            )

            print(
                "\n[OBSERVABILITY] Inference completed.\n"
            )

            return assistant_reply.strip()

        except Exception as e:

            error_message = (
                f"Inference Error: {str(e)}"
            )

            print(error_message)

            return error_message