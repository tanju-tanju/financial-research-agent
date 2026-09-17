import os
import sys
import json
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.bigquery_personas import PERSONAS_RAW

output_file = os.path.join(os.path.dirname(__file__), 'personas.jsonl')
with open(output_file, 'w', encoding='utf-8') as f:
    for p in PERSONAS_RAW:
        row = {
            "persona_id": p["persona_id"],
            "use_case": p["use_case"],
            "name": p["name"],
            "subtitle": p.get("subtitle", ""),
            "branch_or_framework": p.get("branch_or_framework", ""),
            "financial_metrics": json.dumps(p.get("financial_metrics", {})),
            "trigger_or_incident": json.dumps(p.get("trigger_or_incident", {})),
            "payload": json.dumps(p.get("payload", {})),
            "partition_date": time.strftime("%Y-%m-%d"),
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        f.write(json.dumps(row, ensure_ascii=False) + '\n')

print(f"Successfully generated {len(PERSONAS_RAW)} persona rows in {output_file}")
