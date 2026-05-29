import json
import os


MEMORY_FILE = (
    "app/memory/chat_memory.json"
)


def load_memory():

    if not os.path.exists(
        MEMORY_FILE
    ):
        return []

    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return []


def save_memory(history):

    os.makedirs(
        os.path.dirname(MEMORY_FILE),
        exist_ok=True
    )

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=2
        )


def add_message(
    role,
    content
):

    history = load_memory()

    history.append({

        "role": role,

        "content": content
    })

    history = history[-20:]

    save_memory(
        history
    )


def get_history():

    return load_memory()


def clear_memory():

    save_memory([])
