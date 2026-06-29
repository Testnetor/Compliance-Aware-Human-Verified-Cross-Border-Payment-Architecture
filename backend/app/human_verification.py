"""
Human verification module.

This module simulates a Humanode-inspired proof-of-human verification layer.
The goal is to prevent bot-driven abuse, fake accounts, and Sybil-style attacks
before a transfer request reaches the compliance and settlement layers.

Important:
- This is an educational prototype.
- It does not perform real biometric verification.
- It does not replace KYC, AML, or sanctions screening.
- It only models the idea of requiring proof-of-human verification before transfer.
"""

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class HumanVerificationResult:
    wallet: str
    human_verified: bool
    provider: str
    checked_at: str
    reason: str


# Mock database of wallets that passed proof-of-human verification.
# In a future version, this can be replaced with a real Humanode/Biomapper check.
MOCK_HUMAN_VERIFIED_WALLETS = {
    "0x1234567890abcdef": True,
    "0xabcdef1234567890": True,
    "0xbot00000000000000": False,
    "0xfake1111111111111": False,
}


def normalize_wallet(wallet: str) -> str:
    """
    Normalize a wallet address for consistent lookup.

    Args:
        wallet: Wallet address as a string.

    Returns:
        Lowercase wallet address.
    """
    if not wallet or not isinstance(wallet, str):
        raise ValueError("Wallet address must be a non-empty string.")

    return wallet.strip().lower()


def check_human_verification(wallet: str) -> HumanVerificationResult:
    """
    Check whether a wallet has passed proof-of-human verification.

    Args:
        wallet: Wallet address.

    Returns:
        HumanVerificationResult object.
    """
    normalized_wallet = normalize_wallet(wallet)
    is_verified = MOCK_HUMAN_VERIFIED_WALLETS.get(normalized_wallet, False)

    if is_verified:
        reason = "Wallet passed proof-of-human verification."
    else:
        reason = "Wallet is not human-verified. Transfer must be blocked."

    return HumanVerificationResult(
        wallet=normalized_wallet,
        human_verified=is_verified,
        provider="Humanode-inspired mock verification",
        checked_at=datetime.now(timezone.utc).isoformat(),
        reason=reason,
    )


def require_human_verification(wallet: str) -> HumanVerificationResult:
    """
    Require proof-of-human verification before allowing a transfer.

    Args:
        wallet: Wallet address.

    Returns:
        HumanVerificationResult if verification passed.

    Raises:
        PermissionError: If wallet is not human-verified.
    """
    result = check_human_verification(wallet)

    if not result.human_verified:
        raise PermissionError(result.reason)

    return result


if __name__ == "__main__":
    sample_wallet = "0x1234567890abcdef"
    result = check_human_verification(sample_wallet)
    print(result)
