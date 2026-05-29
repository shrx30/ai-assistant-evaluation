from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine

# ---------------------------------
# Presidio Setup
# ---------------------------------

try:
    config = {
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}]
    }
    provider = NlpEngineProvider(nlp_configuration=config)
    nlp_engine = provider.create_engine()

    analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
    anonymizer = AnonymizerEngine()

    PRESIDIO_AVAILABLE = True

except Exception as e:
    print(f"Presidio Init Error: {e}")
    PRESIDIO_AVAILABLE = False


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

    # ---------------------------------
    # Keyword Safety
    # ---------------------------------

    for pattern in BLOCKED_PATTERNS:
        if pattern in prompt_lower:
            return {
                "safe": False,
                "reason": "Unsafe cybersecurity request detected.",
                "sanitized_prompt": None
            }

    # ---------------------------------
    # Presidio Optional
    # ---------------------------------

    if not PRESIDIO_AVAILABLE:
        return {
            "safe": True,
            "reason": "Presidio unavailable.",
            "sanitized_prompt": prompt
        }

    try:
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

    except Exception as e:
        return {
            "safe": True,
            "reason": f"Guardrail fallback: {str(e)}",
            "sanitized_prompt": prompt
        }