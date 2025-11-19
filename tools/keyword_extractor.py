import re
from collections import Counter

def extract_keywords(text, top_k=5):
    """
    Very simple keyword extractor: tokenizes, removes short words,
    counts frequency, and returns top_k tokens.
    """
    if not text:
        return []

    tokens = [
        re.sub(r"[^a-z0-9']", "", t).lower()
        for t in text.split()
        if len(t) > 2
    ]
    counts = Counter(tokens)

    # remove common stop-like words if present
    for w in ["the", "and", "for", "with", "that", "this", "are", "was", "have", "has", "you"]:
        if w in counts:
            del counts[w]

    return [tok for tok, _ in counts.most_common(top_k)]
