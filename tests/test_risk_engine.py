"""
Tests for the compliance risk scoring engine.
"""

import pytest

from backend.app.risk_engine import (
    TransactionRiskInput,
    assess_transaction_risk,
    calculate_amount_risk,
    calculate_country_corridor_risk,
    calculate_frequency_risk,
)


def test_low_risk_transaction_is_approved():
    transaction = TransactionRiskInput(
        transaction_id="TX-001",
        amount_usd=1000,
        sender_country="Turkey",
        destination_country="Italy",
        kyc_status="Verified",
        human_verified=True,
        sanctions_match=False,
        recent_transaction_count=1,
    )

    result = assess_transaction_risk(transaction)

    assert result.transaction_id == "TX-001"
    assert result.risk_level == "Low"
    assert result.decision == "Approved"
    assert result.risk_score <= 30


def test_missing_kyc_increases_risk():
    transaction = TransactionRiskInput(
        transaction_id="TX-002",
        amount_usd=1000,
        sender_country="Turkey",
        destination_country="Italy",
        kyc_status="Missing",
        human_verified=True,
        sanctions_match=False,
        recent_transaction_count=1,
    )

    result = assess_transaction_risk(transaction)

    assert result.risk_score > 30
    assert result.decision in ["Manual Review", "Rejected"]


def test_sanctions_match_is_rejected():
    transaction = TransactionRiskInput(
        transaction_id="TX-003",
        amount_usd=500,
        sender_country="Turkey",
        destination_country="Italy",
        kyc_status="Verified",
        human_verified=True,
        sanctions_match=True,
        recent_transaction_count=1,
    )

    result = assess_transaction_risk(transaction)

    assert result.decision == "Rejected"
    assert result.risk_score >= 60


def test_unverified_human_increases_risk():
    transaction = TransactionRiskInput(
        transaction_id="TX-004",
        amount_usd=1000,
        sender_country="Turkey",
        destination_country="Italy",
        kyc_status="Verified",
        human_verified=False,
        sanctions_match=False,
        recent_transaction_count=1,
    )

    result = assess_transaction_risk(transaction)

    assert result.risk_score > 30
    assert "Human verification missing" in " ".join(result.reasons)


def test_high_amount_has_high_amount_risk():
    points, reason = calculate_amount_risk(15000)

    assert points == 30
    assert reason == "High amount risk"


def test_invalid_amount_raises_error():
    with pytest.raises(ValueError):
        calculate_amount_risk(0)


def test_low_risk_country_corridor():
    points, reason = calculate_country_corridor_risk("Turkey", "Italy")

    assert points == 5
    assert reason == "Low-risk country corridor"


def test_high_risk_country_corridor():
    points, reason = calculate_country_corridor_risk(
        "Turkey",
        "sanctioned-country",
    )

    assert points == 30
    assert reason == "High-risk country corridor"


def test_suspicious_transaction_frequency():
    points, reason = calculate_frequency_risk(15)

    assert points == 25
    assert reason == "Suspicious transaction frequency"


def test_negative_transaction_frequency_raises_error():
    with pytest.raises(ValueError):
        calculate_frequency_risk(-1)
