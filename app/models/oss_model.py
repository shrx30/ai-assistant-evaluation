from transformers import pipeline

pipe = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct"
)

def generate_response(prompt):

    response = pipe(
        prompt,
        max_new_tokens=80
    )

    generated_text = response[0]["generated_text"]

    assistant_reply = generated_text[len(prompt):]

    return assistant_reply.strip()