import datetime, uuid
from tools.text_cleaner import clean_text
from tools.taxonomy import classify_text

AGENT_NAME = "crime_classifier"

def run(bus):
    # Fetch all unprocessed case packets
    packets = bus.get_unprocessed(AGENT_NAME, msg_type="case_packet")
    if not packets:
        return False

    for p in packets:
        text = p["payload"]["description"]
        cleaned = clean_text(text)
        labels = classify_text(cleaned)

        out_msg = {
            "message_id": f"class-{uuid.uuid4().hex[:6]}",
            "timestamp": datetime.datetime.now().isoformat(),
            "sender": AGENT_NAME,
            "type": "classified_packet",
            "payload": {
                "original_id": p["payload"].get("id"),
                "location": p["payload"].get("location"),
                "clean_text": cleaned,
                "labels": labels,
                "source": p["payload"]["source"]
            },
            "provenance": {"parent": p["message_id"]}
        }

        bus.send(out_msg)

    # Mark processed
    bus.mark_processed(AGENT_NAME, [p["message_id"] for p in packets])
    return True
