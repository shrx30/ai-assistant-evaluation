from transformers import (
    pipeline,
    AutoTokenizer
)

from opentelemetry import trace

from telemetry import tracer


MODEL_NAME ="Qwen/Qwen2.5-0.5B-Instruct"


# ----------------------------------------
# Load tokenizer
# ----------------------------------------

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)


# ----------------------------------------
# Load generation pipeline
# ----------------------------------------

pipe = pipeline(
    "text-generation",
    model=MODEL_NAME,
    tokenizer=tokenizer
)


# ----------------------------------------
# Generate response
# ----------------------------------------

def generate_response(messages):

    print("\n[OBSERVABILITY] Starting inference...\n")
    print("GENERATE_RESPONSE FUNCTION CALLED")

    with tracer.start_as_current_span(
        "oss_model_inference"
    ) as span:

        span.set_attribute(
            "model.name",
            MODEL_NAME
        )

        span.set_attribute(
            "conversation.length",
            len(messages)
        )

        prompt = tokenizer.apply_chat_template(

            messages,

            tokenize=False,

            add_generation_prompt=True
        )

        response = pipe(

            prompt,

            max_new_tokens=120,

            temperature=0.7,

            do_sample=True,

            truncation=True
        )

        generated_text = response[0][
            "generated_text"
        ]

        assistant_reply = generated_text[
            len(prompt):
        ]

        span.set_attribute(
            "response.length",
            len(assistant_reply)
        )

        print("\n[OBSERVABILITY] Inference completed.\n")

        return assistant_reply.strip()