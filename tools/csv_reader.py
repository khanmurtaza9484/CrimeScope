def read_csv_text(csv_text):
    """
    Lightweight CSV reader for small demo files.
    Returns a list of dict rows (header -> value).
    """
    lines = [l.strip() for l in csv_text.strip().splitlines() if l.strip()]
    if not lines:
        return []

    header = [h.strip() for h in lines[0].split(",")]
    rows = []
    for line in lines[1:]:
        parts = [p.strip() for p in line.split(",")]
        # pad if columns missing
        while len(parts) < len(header):
            parts.append("")
        row = dict(zip(header, parts))
        rows.append(row)
    return rows
