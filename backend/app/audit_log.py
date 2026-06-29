"""
Audit log system for simulated cross-border payment decisions.

This module records important transfer events and compliance decisions.
In real financial systems, audit logs are essential for traceability,
regulatory review, internal investigation, and operational transparency.

Important:
- This is an educational prototype.
- Logs are stored in memory by default.
- Future versions can store logs in SQLite, PostgreSQL, or external logging systems.
"""

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional
import hashlib
import json


@dataclass
class AuditLogEntry:
    transaction_id: str
    sender_wallet: str
    recipient_wallet: str
    amount_usd: float
    route: str
    human_verified: bool
    kyc_status: str
    sanctions_screening: str
    risk_score: int
    risk_level: str
    decision: str
    estimated_fee_usd: float
    estimated_settlement_hours: float
    timestamp: str
    simulated_transaction_hash: str
    notes: Optional[str] = None


AUDIT_LOGS: list[AuditLogEntry] = []


def generate_simulated_transaction_hash(transaction_id: str, timestamp: str) -> str:
    """
    Generate a simulated transaction hash for audit purposes.

    Args:
        transaction_id: Unique transaction identifier.
        timestamp: ISO timestamp.

    Returns:
        A mock transaction hash string.
    """
    raw_data = f"{transaction_id}-{timestamp}".encode("utf-8")
    return "0x" + hashlib.sha256(raw_data).hexdigest()


def create_audit_log_entry(
    transaction_id: str,
    sender_wallet: str,
    recipient_wallet: str,
    amount_usd: float,
    route: str,
    human_verified: bool,
    kyc_status: str,
    sanctions_screening: str,
    risk_score: int,
    risk_level: str,
    decision: str,
    estimated_fee_usd: float,
    estimated_settlement_hours: float,
    notes: Optional[str] = None,
) -> AuditLogEntry:
    """
    Create and store an audit log entry.

    Args:
        transaction_id: Unique transaction identifier.
        sender_wallet: Sender wallet address.
        recipient_wallet: Recipient wallet address.
        amount_usd: Transfer amount in USD.
        route: Selected settlement route.
        human_verified: Whether proof-of-human verification passed.
        kyc_status: KYC/KYB status.
        sanctions_screening: Sanctions-screening result.
        risk_score: Numeric compliance risk score.
        risk_level: Low, Medium, or High.
        decision: Approved, Manual Review, or Rejected.
        estimated_fee_usd: Estimated transaction fee.
        estimated_settlement_hours: Estimated settlement duration.
        notes: Optional additional notes.

    Returns:
        AuditLogEntry object.
    """
    if amount_usd <= 0:
        raise ValueError("Amount must be greater than zero.")

    if risk_score < 0 or risk_score > 100:
        raise ValueError("Risk score must be between 0 and 100.")

    timestamp = datetime.now(timezone.utc).isoformat()
    simulated_hash = generate_simulated_transaction_hash(
        transaction_id,
        timestamp,
    )

    entry = AuditLogEntry(
        transaction_id=transaction_id,
        sender_wallet=sender_wallet.lower(),
        recipient_wallet=recipient_wallet.lower(),
        amount_usd=amount_usd,
        route=route,
        human_verified=human_verified,
        kyc_status=kyc_status,
        sanctions_screening=sanctions_screening,
        risk_score=risk_score,
        risk_level=risk_level,
        decision=decision,
        estimated_fee_usd=estimated_fee_usd,
        estimated_settlement_hours=estimated_settlement_hours,
        timestamp=timestamp,
        simulated_transaction_hash=simulated_hash,
        notes=notes,
    )

    AUDIT_LOGS.append(entry)
    return entry


def get_all_audit_logs() -> list[dict]:
    """
    Return all audit logs as dictionaries.
    """
    return [asdict(entry) for entry in AUDIT_LOGS]


def get_audit_log_by_transaction_id(transaction_id: str) -> Optional[dict]:
    """
    Find an audit log by transaction ID.

    Args:
        transaction_id: Unique transaction identifier.

    Returns:
        Audit log dictionary if found, otherwise None.
    """
    for entry in AUDIT_LOGS:
        if entry.transaction_id == transaction_id:
            return asdict(entry)

    return None


def export_audit_logs_to_json() -> str:
    """
    Export all audit logs as formatted JSON.

    Returns:
        JSON string.
    """
    return json.dumps(get_all_audit_logs(), indent=2)


def clear_audit_logs() -> None:
    """
    Clear in-memory audit logs.

    Mainly useful for tests.
    """
    AUDIT_LOGS.clear()


if __name__ == "__main__":
    sample_entry = create_audit_log_entry(
        transaction_id="TX-001",
        sender_wallet="0x1234567890abcdef",
        recipient_wallet="0xabcdef1234567890",
        amount_usd=1000,
        route="stablecoin",
        human_verified=True,
        kyc_status="Verified",
        sanctions_screening="Passed",
        risk_score=22,
        risk_level="Low",
        decision="Approved",
        estimated_fee_usd=0.45,
        estimated_settlement_hours=0.5,
        notes="Educational simulated transfer.",
    )

    print(sample_entry)
    print(export_audit_logs_to_json())
