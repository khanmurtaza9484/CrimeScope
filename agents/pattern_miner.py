import datetime, uuid
from tools.keyword_extractor import extract_keywords

AGENT_NAME = "pattern_miner"

def run(bus):
    # Get all unprocessed classified packets
    packets = bus.get_unprocessed(AGENT_NAME, msg_type="classified_packet")
    if not packets:
        return False

    for p in packets:
        text = p["payload"]["clean_text"]
        labels = p["payload"]["labels"]

        keywords = extract_keywords(text)
        
        out_msg = {
            "message_id": f"pattern-{uuid.uuid4().hex[:6]}",
            "timestamp": datetime.datetime.now().isoformat(),
            "sender": AGENT_NAME,
            "type": "pattern_packet",
            "payload": {
                "original_id": p["payload"].get("original_id"),
                "location": p["payload"].get("location"),
                "labels": labels,
                "keywords": keywords
            },
            "provenance": {"parent": p["message_id"]}
        }

        bus.send(out_msg)

    # mark processed
    bus.mark_processed(AGENT_NAME, [p["message_id"] for p in packets])
    return True
