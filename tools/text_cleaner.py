import re

def clean_text(text):
    """
    Simple normalizer for crime descriptions.
    Lowercases, removes extra spaces, punctuation, and newlines.
    """
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)  # remove punctuation
    text = re.sub(r"\s+", " ", text)         # collapse whitespace
    return text.strip()
