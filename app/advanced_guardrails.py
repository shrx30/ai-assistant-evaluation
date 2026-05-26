from presidio_analyzer import AnalyzerEngine

from presidio_anonymizer import (
    AnonymizerEngine
)


# ---------------------------------
# Presidio Setup
# ---------------------------------

analyzer = AnalyzerEngine()

anonymizer = AnonymizerEngine()


# ---------------------------------
# Unsafe Prompt Patterns
# ---------------------------------

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


# ---------------------------------
# Main Guardrail Function
# ---------------------------------

def guardrail_check(prompt):

    prompt_lower = prompt.lower()

    # Keyword safety

    for pattern in BLOCKED_PATTERNS:

        if pattern in prompt_lower:

            return {

                "safe": False,

                "reason": "Unsafe cybersecurity request detected.",

                "sanitized_prompt": None
            }

    # PII detection

    results = analyzer.analyze(

        text=prompt,

        language="en"
    )

    sanitized = anonymizer.anonymize(

        text=prompt,

        analyzer_results=results
    )

    sanitized_text = sanitized.text

    return {

        "safe": True,

        "reason": "Prompt passed safety checks.",

        "sanitized_prompt": sanitized_text
    }