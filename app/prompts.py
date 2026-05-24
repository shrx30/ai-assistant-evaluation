SYSTEM_PROMPT = """
You are a helpful, concise, and safe AI assistant.
"""

def build_prompt(history, user_input):

    prompt = SYSTEM_PROMPT + "\n\n"

    for message in history:

        role = message["role"]
        content = message["content"]

        prompt += f"{role}: {content}\n"

    prompt += f"user: {user_input}\nassistant:"

    return prompt