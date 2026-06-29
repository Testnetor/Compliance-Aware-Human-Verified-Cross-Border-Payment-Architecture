"""
Compliance risk scoring engine.

This module calculates a simplified compliance risk score for simulated
cross-border payment requests.

The goal is to demonstrate regulatory-aware engineering thinking:
a payment system should not only optimize for cost and speed, but also
evaluate security, compliance, and suspicious activity risks.

Important:
- This is an educational prototype.
- It does not use real sanctions data.
- It does not replace professional AML/KYC systems.
- Risk rules are simplified for portfolio and research purposes.
"""

from dataclasses import dataclass


@dataclass
class TransactionRiskInput:
    transaction_id: str
    amount_usd: float
    sender_country: str
    destination_country: str
    kyc_status: str
    human_verified: bool
    sanctions_match: bool
    recent_transaction_count: int


@dataclass
class RiskAssessmentResult:
    transaction_id: str
    risk_score: int
    risk_level: str
    decision: str
    reasons: list[str]


LOW_RISK_COUNTRIES = {
    "turkey",
    "italy",
    "germany",
    "france",
    "spain",
    "netherlands",
}

HIGH_RISK_COUNTRIES = {
    "unknown",
    "high-risk-jurisdiction",
    "sanctioned-country",
}


def normalize_text(value: str) -> str:
    """
    Normalize text values for comparison.
    """
    if not value or not isinstance(value, str):
        return "unknown"

    return value.strip().lower()


def calculate_amount_risk(amount_usd: float) -> tuple[int, str]:
    """
    Calculate risk points based on transaction amount.
    """
    if amount_usd <= 0:
        raise ValueError("Amount must be greater than zero.")

    if amount_usd < 1000:
        return 5, "Low amount risk"

    if amount_usd <= 10000:
        return 15, "Medium amount risk"

    return 30, "High amount risk"


def calculate_country_corridor_risk(
    sender_country: str,
    destination_country: str,
) -> tuple[int, str]:
    """
    Calculate risk points based on sender and destination countries.
    """
    sender = normalize_text(sender_country)
    destination = normalize_text(destination_country)

    if sender in HIGH_RISK_COUNTRIES or destination in HIGH_RISK_COUNTRIES:
        return 30, "High-risk country corridor"

    if sender in LOW_RISK_COUNTRIES and destination in LOW_RISK_COUNTRIES:
        return 5, "Low-risk country corridor"

    return 15, "Medium-risk country corridor"


def calculate_frequency_risk(recent_transaction_count: int) -> tuple[int, str]:
    """
    Calculate risk points based on recent transaction frequency.
    """
    if recent_transaction_count < 0:
        raise ValueError("Recent transaction count cannot be negative.")

    if recent_transaction_count <= 3:
        return 0, "Normal transaction frequency"

    if recent_transaction_count <= 10:
        return 10, "Elevated transaction frequency"

    return 25, "Suspicious transaction frequency"


def determine_risk_level(score: int) -> str:
    """
    Convert numeric risk score into a risk level.
    """
    if score <= 30:
        return "Low"

    if score <= 70:
        return "Medium"

    return "High"


def determine_decision(risk_level: str, sanctions_match: bool) -> str:
    """
    Determine final compliance decision.
    """
    if sanctions_match:
        return "Rejected"

    if risk_level == "Low":
        return "Approved"

    if risk_level == "Medium":
        return "Manual Review"

    return "Rejected"


def assess_transaction_risk(
    risk_input: TransactionRiskInput,
) -> RiskAssessmentResult:
    """
    Assess transaction risk using simplified compliance rules.
    """
    score = 0
    reasons: list[str] = []

    # Human verification
    if risk_input.human_verified:
        score -= 10
        reasons.append("Human verification passed: -10 points")
    else:
        score += 25
        reasons.append("Human verification missing: +25 points")

    # KYC/KYB status
    kyc_status = normalize_text(risk_input.kyc_status)

    if kyc_status == "verified":
        reasons.append("KYC/KYB verified: +0 points")
    elif kyc_status == "pending":
        score += 15
        reasons.append("KYC/KYB pending: +15 points")
    elif kyc_status == "missing":
        score += 30
        reasons.append("KYC/KYB missing: +30 points")
    else:
        score += 25
        reasons.append("Unknown KYC/KYB status: +25 points")

    # Sanctions screening
    if risk_input.sanctions_match:
        score += 60
        reasons.append("Sanctions match detected: +60 points")
    else:
        reasons.append("Sanctions screening passed: +0 points")

    # Amount risk
    amount_points, amount_reason = calculate_amount_risk(risk_input.amount_usd)
    score += amount_points
    reasons.append(f"{amount_reason}: +{amount_points} points")

    # Country corridor risk
    corridor_points, corridor_reason = calculate_country_corridor_risk(
        risk_input.sender_country,
        risk_input.destination_country,
    )
    score += corridor_points
    reasons.append(f"{corridor_reason}: +{corridor_points} points")

    # Frequency risk
    frequency_points, frequency_reason = calculate_frequency_risk(
        risk_input.recent_transaction_count
    )
    score += frequency_points
    reasons.append(f"{frequency_reason}: +{frequency_points} points")

    # Keep score inside 0-100 range
    score = max(0, min(score, 100))

    risk_level = determine_risk_level(score)
    decision = determine_decision(risk_level, risk_input.sanctions_match)

    return RiskAssessmentResult(
        transaction_id=risk_input.transaction_id,
        risk_score=score,
        risk_level=risk_level,
        decision=decision,
        reasons=reasons,
    )


if __name__ == "__main__":
    sample = TransactionRiskInput(
        transaction_id="TX-001",
        amount_usd=1000,
        sender_country="Turkey",
        destination_country="Italy",
        kyc_status="Verified",
        human_verified=True,
        sanctions_match=False,
        recent_transaction_count=1,
    )

    result = assess_transaction_risk(sample)
    print(result)
