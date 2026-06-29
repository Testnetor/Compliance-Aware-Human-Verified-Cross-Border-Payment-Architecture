"""
Fee and latency calculator for cross-border payment routes.

This module compares traditional SWIFT-based banking with stablecoin-based
settlement using simplified educational assumptions.

Assumptions:
- SWIFT fee ratio: 4.5%
- Stablecoin fee ratio: 0.045%
- SWIFT settlement time: 72 hours
- Stablecoin settlement time: 0.5 hours
"""

from dataclasses import dataclass


@dataclass
class PaymentRouteResult:
    route: str
    amount_usd: float
    fee_ratio_percent: float
    estimated_fee_usd: float
    estimated_received_usd: float
    estimated_settlement_hours: float


SWIFT_FEE_RATIO = 4.5
STABLECOIN_FEE_RATIO = 0.045

SWIFT_SETTLEMENT_HOURS = 72
STABLECOIN_SETTLEMENT_HOURS = 0.5


def calculate_fee(amount_usd: float, fee_ratio_percent: float) -> float:
    """
    Calculate the transaction fee.

    Args:
        amount_usd: Transfer amount in USD.
        fee_ratio_percent: Fee percentage.

    Returns:
        Fee amount in USD.
    """
    if amount_usd <= 0:
        raise ValueError("Amount must be greater than zero.")

    if fee_ratio_percent < 0:
        raise ValueError("Fee ratio cannot be negative.")

    return amount_usd * (fee_ratio_percent / 100)


def calculate_route_result(route: str, amount_usd: float) -> PaymentRouteResult:
    """
    Calculate fee, received amount, and settlement time for a payment route.

    Args:
        route: Payment route. Supported values: "swift", "stablecoin".
        amount_usd: Transfer amount in USD.

    Returns:
        PaymentRouteResult object.
    """
    route = route.lower()

    if route == "swift":
        fee_ratio = SWIFT_FEE_RATIO
        settlement_hours = SWIFT_SETTLEMENT_HOURS
        route_name = "Traditional SWIFT-based banking"

    elif route == "stablecoin":
        fee_ratio = STABLECOIN_FEE_RATIO
        settlement_hours = STABLECOIN_SETTLEMENT_HOURS
        route_name = "Stablecoin-based settlement"

    else:
        raise ValueError("Unsupported route. Use 'swift' or 'stablecoin'.")

    estimated_fee = calculate_fee(amount_usd, fee_ratio)
    estimated_received = amount_usd - estimated_fee

    return PaymentRouteResult(
        route=route_name,
        amount_usd=amount_usd,
        fee_ratio_percent=fee_ratio,
        estimated_fee_usd=round(estimated_fee, 2),
        estimated_received_usd=round(estimated_received, 2),
        estimated_settlement_hours=settlement_hours,
    )


def compare_routes(amount_usd: float) -> dict:
    """
    Compare SWIFT and stablecoin payment routes.

    Args:
        amount_usd: Transfer amount in USD.

    Returns:
        Dictionary containing both route results and improvement metrics.
    """
    swift_result = calculate_route_result("swift", amount_usd)
    stablecoin_result = calculate_route_result("stablecoin", amount_usd)

    time_saved_hours = (
        swift_result.estimated_settlement_hours
        - stablecoin_result.estimated_settlement_hours
    )

    fee_saved_usd = (
        swift_result.estimated_fee_usd
        - stablecoin_result.estimated_fee_usd
    )

    fee_reduction_percent = (
        fee_saved_usd / swift_result.estimated_fee_usd
    ) * 100

    time_reduction_percent = (
        time_saved_hours / swift_result.estimated_settlement_hours
    ) * 100

    return {
        "amount_usd": amount_usd,
        "swift": swift_result.__dict__,
        "stablecoin": stablecoin_result.__dict__,
        "comparison": {
            "fee_saved_usd": round(fee_saved_usd, 2),
            "time_saved_hours": round(time_saved_hours, 2),
            "fee_reduction_percent": round(fee_reduction_percent, 2),
            "time_reduction_percent": round(time_reduction_percent, 2),
        },
    }


if __name__ == "__main__":
    result = compare_routes(1000)
    print(result)
