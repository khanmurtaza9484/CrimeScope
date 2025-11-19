import datetime, json, os

AGENT_NAME = "report_writer"

def run(bus):
    # collect relevant messages
    classified = bus.query(lambda m: m.get("type") == "classified_packet")
    patterns = bus.query(lambda m: m.get("type") == "pattern_packet")
    hotspots = bus.query(lambda m: m.get("type") == "hotspot_packet")
    risks = bus.query(lambda m: m.get("type") == "risk_packet")

    # pick last risk factors
    risk_factors = risks[-1]["payload"]["risk_factors"] if risks else []

    # assemble summary text
    summary = f"Report generated {datetime.datetime.now().isoformat()}\n"
    summary += f"Classified incidents: {len(classified)}\n"
    summary += f"Extracted pattern entries: {len(patterns)}\n"
    summary += f"Hotspots detected: {len(hotspots)}\n"
    summary += f"Top risk factors: {len(risk_factors)}\n"

    # prepare final data
    report_data = {
        "summary": summary,
        "risk_factors": risk_factors,
        "patterns": [m["payload"] for m in patterns],
        "hotspots": [m["payload"] for m in hotspots]
    }

    # ensure demo folder exists
    os.makedirs("demo", exist_ok=True)

    # write Markdown
    md_path = "demo/crimescope_report.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# CrimeScope Report\n\n")
        f.write("## Summary\n")
        f.write(summary + "\n")
        f.write("## Risk Factors\n")
        for rf in risk_factors:
            f.write(f"- {rf['crime_label']} in {rf['location_bucket']} (count: {rf['count']})\n")
        f.write("\n## Patterns\n")
        for p in patterns:
            f.write(f"- ID: {p['payload']['original_id']}, keywords: {p['payload']['keywords']}\n")
        f.write("\n## Hotspots\n")
        for h in hotspots:
            f.write(f"- Bucket: {h['payload']['bucket']}, raw location: {h['payload']['location']}\n")

    # write JSON
    json_path = "demo/crimescope_report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

    return report_data
