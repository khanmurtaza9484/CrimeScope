# 🔍 CrimeScope  
### Multi-Agent Crime Intelligence System (Kaggle AI Agents Capstone Project)

CrimeScope is a lightweight, fully modular **multi-agent system** that analyzes crime reports and news articles to identify:

- crime classifications  
- hotspots  
- pattern keywords  
- risk factor correlations  

This project is built for the **Kaggle x Google 5-Day AI Agents Intensive Capstone Project**.
---

## 🧠 What CrimeScope Does

CrimeScope uses a pipeline of specialized agents:

| Agent | Purpose |
|-------|---------|
| **Data Intake Agent** | Ingests CSV data + news text |
| **Crime Classifier Agent** | Classifies incidents using a keyword taxonomy |
| **Pattern Miner Agent** | Extracts keywords & recurring patterns |
| **Hotspot Detector Agent** | Groups incidents by geo buckets |
| **Risk Factor Agent** | Finds co-occurrence correlations |
| **Report Writer Agent** | Produces Markdown + JSON reports |

At the end, CrimeScope generates:

demo/crimescope_report.md  
demo/crimescope_report.json

---

## 🏗️ Architecture Overview

```
data_intake
   ↓
crime_classifier
   ↓
pattern_miner
   ↓
hotspot_detector
   ↓
risk_factor
   ↓
report_writer
```

CrimeScope uses a **Persistent A2A Message Bus**, which stores:

- all agent messages  
- provenance trails  
- processed_by metadata  
- typed events (case_packet, classified_packet, pattern, hotspot, risk, etc.)

This enables multi-agent collaboration without central logic.
---

## 📂 Project Structure

CrimeScope/
main.py
agents/
data_intake.py
crime_classifier.py
pattern_miner.py
hotspot_detector.py
risk_factor.py
report_writer.py
tools/
csv_reader.py
text_cleaner.py
taxonomy.py
keyword_extractor.py
geo_utils.py
demo/
sample_data.csv
sample_news.txt
crimescope_report.md (generated after running main.py)
crimescope_report.json (generated after running main.py)
README.md
LICENSE
---

## ▶️ How to Run

### **1. Clone the repository**

```bash
git clone https://github.com/khanmurtaza9484/CrimeScope.git
cd CrimeScope
2. Run the project
python main.py


If everything is correct, you will see:

Starting CrimeScope demo...
Report Summary: ...


And two files will be created:

demo/crimescope_report.md
demo/crimescope_report.json---

## 🧪 Demo Data

The `demo/` folder contains:

- **sample_data.csv** → 4 crime incidents  
- **sample_news.txt** → cyberattack news snippet  

These are automatically processed into the final report.
---

## 📜 License

This project is released under **CC BY 4.0**.  
You may share and remix with attribution.
---

## ✨ Author

**CrimeScope**  
Built by **Mohammad Murtaza Khan**  
For *Kaggle x Google — 5-Day AI Agents Intensive (Capstone Project)*
