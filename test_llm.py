from transformers import pipeline

pipe = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct"
)

conversation = []

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    conversation.append(f"User: {user_input}")

    prompt = "\n".join(conversation)
    prompt += "\nAssistant:"

    response = pipe(
        prompt,
        max_new_tokens=80
    )

    generated_text = response[0]["generated_text"]

    assistant_reply = generated_text[len(prompt):]

    print("\nAssistant:")
    print(assistant_reply.strip())
    print()

    conversation.append(f"Assistant: {assistant_reply.strip()}")