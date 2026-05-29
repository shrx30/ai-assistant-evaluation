import json
import os
from memory.memory_summarizer import summarize_history

# =================================
# MEMORY FILE
# =================================

MEMORY_FILE = "app/memory/chat_memory.json"
SUMMARY_FILE = "app/memory/summary_memory.txt"


# =================================
# LOAD MEMORY
# =================================

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []


# =================================
# SAVE MEMORY
# =================================

def save_memory(history):
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=2)


def save_summary(summary):
    with open(SUMMARY_FILE, "w", encoding="utf-8") as file:
        file.write(summary)


def load_summary():
    if not os.path.exists(SUMMARY_FILE):
        return ""
    try:
        with open(SUMMARY_FILE, "r", encoding="utf-8") as file:
            return file.read()
    except Exception:
        return ""


# =================================
# ADD MESSAGE
# =================================

def add_message(role, content):
    history = load_memory()
    history.append({
        "role": role,
        "content": content
    })

    # -----------------------------
    # MEMORY TRUNCATION
    # -----------------------------

    if len(history) > 20:
        old_history = history[:-20]
        summary = summarize_history(old_history)
        save_summary(summary)
        history = history[-20:]

    # FIX: always save memory
    save_memory(history)


# =========================