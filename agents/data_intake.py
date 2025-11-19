import uuid, datetime
from tools.csv_reader import read_csv_text
from tools.text_cleaner import clean_text

def run(csv_text, news_text, bus):
    # Process CSV rows
    rows = read_csv_text(csv_text)
    for row in rows:
        pid = f"csv-{row.get('id') or uuid.uuid4().hex[:6]}"

        packet = {
            "message_id": pid,
            "timestamp": datetime.datetime.now().isoformat(),
            "sender": "data_intake",
            "type": "case_packet",
            "payload": {
                "id": row.get("id"),
                "date": row.get("date"),
                "location": row.get("location"),
                "description": row.get("description"),
                "source": "csv"
            },
            "provenance": {"source": "csv"}
        }

        bus.send(packet)

    # Process news article text
    news_clean = clean_text(news_text)
    news_packet = {
        "message_id": f"news-{uuid.uuid4().hex[:6]}",
        "timestamp": datetime.datetime.now().isoformat(),
        "sender": "data_intake",
        "type": "case_packet",
        "payload": {
            "id": None,
            "date": datetime.date.today().isoformat(),
            "location": "UnknownCity",
            "description": news_clean,
            "source": "news"
        },
        "provenance": {"source": "news"}
    }

    bus.send(news_packet)
    return True
