"""
Tests for the Humanode-inspired human verification module.
"""

import pytest

from backend.app.human_verification import (
    check_human_verification,
    require_human_verification,
)


def test_verified_wallet_passes_human_verification():
    wallet = "0x1234567890abcdef"

    result = check_human_verification(wallet)

    assert result.wallet == wallet
    assert result.human_verified is True
    assert result.provider == "Humanode-inspired mock verification"
    assert "passed" in result.reason.lower()


def test_unverified_wallet_fails_human_verification():
    wallet = "0xbot00000000000000"

    result = check_human_verification(wallet)

    assert result.wallet == wallet
    assert result.human_verified is False
    assert "not human-verified" in result.reason.lower()


def test_unknown_wallet_is_not_verified_by_default():
    wallet = "0xunknownwallet0000"

    result = check_human_verification(wallet)

    assert result.human_verified is False


def test_require_human_verification_allows_verified_wallet():
    wallet = "0xabcdef1234567890"

    result = require_human_verification(wallet)

    assert result.human_verified is True


def test_require_human_verification_blocks_unverified_wallet():
    wallet = "0xfake1111111111111"

    with pytest.raises(PermissionError):
        require_human_verification(wallet)


def test_wallet_normalization_accepts_uppercase_input():
    wallet = "0x1234567890ABCDEF"

    result = check_human_verification(wallet)

    assert result.wallet == "0x1234567890abcdef"
    assert result.human_verified is True
