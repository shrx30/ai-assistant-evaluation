BLOCKED_PATTERNS = [

    "ransomware",
    "phishing",
    "hack wifi",
    "steal passwords",
    "malware",
    "keylogger",
    "ddos",
    "exploit"

]


def guardrail_check(prompt):

    prompt_lower = prompt.lower()

    for pattern in BLOCKED_PATTERNS:

        if pattern in prompt_lower:

            return False, (
                "Request blocked by safety guardrails."
            )

    return True, None