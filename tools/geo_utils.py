import re

def bucket_location(location_text):
    """
    Simple geo-bucketing for demo:
    - "City, State" -> "city"
    - multi-word -> first word or first-last fallback
    - numeric/empty -> "unknown"
    """
    if not location_text:
        return "unknown"
    text = location_text.strip()
    if text.lower() in ["unknown", "n/a", "na", ""]:
        return "unknown"

    # "City, State"
    if "," in text:
        return text.split(",")[0].strip().lower()

    # hyphen/slash
    for sep in ["-", "/"]:
        if sep in text:
            return text.split(sep)[0].strip().lower()

    parts = [p for p in text.split() if not re.match(r"^[0-9]+$", p)]
    if not parts:
        return "unknown"
    if len(parts) == 1:
        return parts[0].lower()
    # prefer first word for common suffix like "park", "town"
    if parts[-1].lower() in ["park", "town", "city", "downtown", "station", "district", "village"]:
        return parts[0].lower()
    return f"{parts[0].lower()}-{parts[-1].lower()}"
