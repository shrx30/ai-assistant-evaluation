BLOCKED_WORDS = [

    "hack",

    "malware",

    "exploit",

    "virus",

    "phishing",

    "ransomware"
]


def is_safe(text):

    text = text.lower()

    for word in BLOCKED_WORDS:

        if word in text:

            return False

    return True
