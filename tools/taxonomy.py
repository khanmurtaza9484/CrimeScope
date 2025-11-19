CRIME_KEYWORDS = {
    "theft": ["steal", "stolen", "theft", "rob", "snatch"],
    "vandalism": ["vandal", "damage", "smashed", "destroy"],
    "cybercrime": ["phishing", "malware", "breach", "ransomware", "cyber"],
    "fraud": ["scam", "fraud", "fake", "deceptive"],
}

def classify_text(text):
    """
    Returns a list of crime labels detected in the text.
    Matches against a simple keyword taxonomy.
    """
    labels = []
    for label, keywords in CRIME_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                labels.append(label)
                break
    return labels
