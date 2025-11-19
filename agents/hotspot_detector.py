import datetime, uuid
from tools.geo_utils import bucket_location

AGENT_NAME = "hotspot_detector"

def run(bus):
    # Retrieve unprocessed classified or pattern packets
    packets = bus.get_unprocessed(AGENT_NAME)
    if not packets:
        return False

    for p in packets:
        location = p["payload"].get("location") or "Unknown"

        bucket = bucket_location(location)

        out_msg = {
            "message_id": f"hot-{uuid.uuid4().hex[:6]}",
            "timestamp": datetime.datetime.now().isoformat(),
            "sender": AGENT_NAME,
            "type": "hotspot_packet",
            "payload": {
                "location": location,
                "bucket": bucket,
                "source_message": p["message_id"]
            },
            "provenance": {"parent": p["message_id"]}
        }

        bus.send(out_msg)

    bus.mark_processed(AGENT_NAME, [p["message_id"] for p in packets])
    return True
