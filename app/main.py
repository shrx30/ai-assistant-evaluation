from memory import add_message, get_context
from prompts import build_prompt
from models.oss_model import generate_response
from telemetry import tracer

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    history = get_context()

    prompt = build_prompt(history, user_input)

    response = generate_response(prompt)

    print("\nAssistant:")
    print(response)
    print()

    add_message("user", user_input)
    add_message("assistant", response)