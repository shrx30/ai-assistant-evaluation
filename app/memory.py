conversation = []

def add_message(role, content):

    conversation.append({
        "role": role,
        "content": content
    })

def get_context(limit=6):

    return conversation[-limit:]