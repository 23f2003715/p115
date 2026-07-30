import os
import json
from datetime import datetime

os.makedirs("logs", exist_ok=True)

LOG_FILE = "logs/run.jsonl"

def log_event(event):
    event["timestamp"] = datetime.now().isoformat()

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

    return LOG_FILE