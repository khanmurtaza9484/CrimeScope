import datetime, uuid
from collections import Counter
from tools.geo_utils import bucket_location

AGENT_NAME = "risk_factor"

def run(bus):
    """
    Detect risk factor co-occurrences (label <-> location bucket).
    Processes classified_packet and hotspot_packet messages that this
    agent hasn't yet processed.
    """
    # gather relevant unprocessed messages
    classified = [m for m in bus.all() if m.get("type") == "classified_packet" and AGENT_NAME not in m.get("processed_by", [])]
    hotspots = [m for m in bus.all() if m.get("type") == "hotspot_packet" and AGENT_NAME not in m.get("processed_by", [])]

    if not classified and not hotspots:
        return False

    # map message_id -> bucket (from hotspot messages) and message_id -> labels (from classified)
    id_to_bucket = {}
    for h in hotspots:
        src = h["payload"].get("source_message")
        b = h["payload"].get("bucket") or bucket_location(h["payload"].get("location",""))
        if src:
            id_to_bucket[src] = b

    pair_counts = Counter()
    for c in classified:
        labels = c["payload"].get("labels") or []
        msg_id = c["message_id"]
        # prefer bucket from hotspot messages, otherwise compute from location
        bucket = id_to_bucket.get(msg_id) or bucket_location(c["payload"].get("location",""))
        # labels might be a list or dict; normalize to list of strings
        if isinstance(labels, dict):
            label_list = list(labels.keys())
        elif isinstance(labels, list):
            label_list = labels
        else:
            label_list = [str(labels)]
        for lab in label_list:
            pair_counts[(lab, bucket)] += 1

    # prepare top risk factors
    top = pair_counts.most_common(10)
    risk_factors = [{"crime_label": lab, "location_bucket": bucket, "count": cnt} for (lab, bucket), cnt in top]

    # publish risk message
    out_msg = {
        "message_id": f"risk-{uuid.uuid4().hex[:6]}",
        "timestamp": datetime.datetime.now().isoformat(),
        "sender": AGENT_NAME,
        "type": "risk_packet",
        "payload": {
            "risk_factors": risk_factors
        },
        "provenance": {}
    }
    bus.send(out_msg)

    # mark processed for the messages we consumed
    processed_ids = [m["message_id"] for m in classified + hotspots]
    bus.mark_processed(AGENT_NAME, processed_ids)

    return risk_factors
