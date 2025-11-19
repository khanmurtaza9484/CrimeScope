import uuid, datetime
from agents.data_intake import run as intake_run
from agents.crime_classifier import run as classifier_run
from agents.pattern_miner import run as pattern_run
from agents.hotspot_detector import run as hotspot_run
from agents.risk_factor import run as risk_run
from agents.report_writer import run as report_run

class PersistentA2ABus:
    def __init__(self):
        self.history = []

    def send(self, message):
        message.setdefault('message_id', f"msg-{uuid.uuid4().hex[:8]}")
        message.setdefault('timestamp', datetime.datetime.now().isoformat())
        message.setdefault('processed_by', [])
        self.history.append(message)

    def get_unprocessed(self, agent_name, msg_type=None):
        msgs = []
        for m in self.history:
            if agent_name in m.get('processed_by', []):
                continue
            if msg_type and m.get('type') != msg_type:
                continue
            msgs.append(m)
        return msgs

    def mark_processed(self, agent_name, message_ids):
        for m in self.history:
            if m['message_id'] in message_ids:
                if 'processed_by' not in m:
                    m['processed_by'] = []
                m['processed_by'].append(agent_name)

    def query(self, fn):
        return [m for m in self.history if fn(m)]

    def all(self):
        return self.history[:]

# --- Demo Inputs ---
demo_csv = """id,date,location,description
1,2025-11-01,Central Park,Shop owner reported a theft; items were stolen from an unattended stall
2,2025-11-02,Downtown,Several cars were vandalized overnight; windows smashed
3,2025-11-03,Old Town,User reported a phishing scam via email; several residents reported fraudulent messages
4,2025-11-05,Central Park,An individual attempted to steal a bike from the park; suspect seen running
"""

demo_news = """
A group of drones with suspected malware triggered a breach in a logistics hub's systems, causing temporary outages. Local authorities suspect a coordinated cyberattack and warn businesses to check for suspicious emails and ransomware indicators.
"""

def main():
    bus = PersistentA2ABus()
    print("Starting CrimeScope demo...")

    intake_run(demo_csv, demo_news, bus)
    classifier_run(bus)
    pattern_run(bus)
    hotspot_run(bus)
    risk_run(bus)

    report = report_run(bus)

    print("\nReport Summary:")
    print(report.get("summary"))
    print("Full report written to demo/crimescope_report.md and demo/crimescope_report.json")

if __name__ == "__main__":
    main()
