"""
BigQuery WORM Immutable Audit Vault
Implements cryptographic SHA-256 hash chaining for agent execution logs
under German GoBD and DORA standards.
"""

import hashlib
import json
import logging
import os
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from app.config import PROJECT_ID, REGION, DATASET_CORE, ADMIN_EMAIL

logger = logging.getLogger("audit_vault")

class AuditVault:
    def __init__(self):
        self.project_id = PROJECT_ID
        self.last_hash = "0" * 64
        self.local_audit_log = os.path.join(os.path.dirname(__file__), "..", "..", "tests", "data", "audit_log.jsonl")
        os.makedirs(os.path.dirname(self.local_audit_log), exist_ok=True)
        self.client = None
        self._init_bq()

    def _init_bq(self):
        try:
            from google.cloud import bigquery
            self.client = bigquery.Client(project=self.project_id, location=REGION)
        except Exception as e:
            logger.info(f"Audit vault using local immutable store: {e}")

    def log_action(
        self,
        case_id: str,
        use_case_typ: str,
        agent_name: str,
        aktions_typ: str,
        prompt_str: str,
        executed_sql: Optional[str],
        latency_ms: int,
        result_payload: Dict[str, Any],
        user_id: str = ADMIN_EMAIL
    ) -> Dict[str, Any]:
        """
        Calculates SHA-256 digital signature chained to the previous entry,
        records the event to BigQuery WORM table, and mirrors to local append-only storage.
        """
        audit_id = str(uuid.uuid4())
        now_utc = datetime.utcnow().isoformat() + "Z"
        prompt_hash = hashlib.sha256(prompt_str.encode("utf-8")).hexdigest()
        payload_str = json.dumps(result_payload, sort_keys=True)

        # Chained cryptographic hash
        signature_material = f"{self.last_hash}|{audit_id}|{now_utc}|{case_id}|{agent_name}|{aktions_typ}|{prompt_hash}|{payload_str}"
        digital_signature = hashlib.sha256(signature_material.encode("utf-8")).hexdigest()
        self.last_hash = digital_signature

        record = {
            "audit_id": audit_id,
            "zeitstempel": now_utc,
            "case_id": case_id,
            "use_case_typ": use_case_typ,
            "agent_name": agent_name,
            "aktions_typ": aktions_typ,
            "eingabe_prompt_hash": prompt_hash,
            "ausgefuehrte_sql": executed_sql,
            "abfrage_latenz_ms": latency_ms,
            "anzahl_zeilen_ergebnis": 1 if result_payload else 0,
            "ergebnis_payload_json": payload_str,
            "sha256_digitale_signatur": digital_signature,
            "akteur_benutzer_id": user_id
        }

        # Local append-only ledger
        try:
            with open(self.local_audit_log, "a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
        except Exception as ex:
            logger.error(f"Local audit log write failed: {ex}")

        # Stream to BigQuery WORM table
        if self.client:
            try:
                table_id = f"{self.project_id}.{DATASET_CORE}.audit_agent_execution_log"
                errors = self.client.insert_rows_json(table_id, [record])
                if errors:
                    logger.warning(f"BigQuery WORM stream errors: {errors}")
            except Exception as bq_ex:
                logger.warning(f"BigQuery WORM stream exception: {bq_ex}")

        return record

    def get_latest_hash(self) -> str:
        return self.last_hash
