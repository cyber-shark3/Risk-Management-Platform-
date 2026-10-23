from decimal import Decimal as D

import pytest

from risk_engine.position_sizing import calculate_position_size


def base(**overrides):
    args = dict(
        equity=D("10000"),
        risk_percent=D("1"),
        entry_price=D("100"),
        stop_loss=D("95"),
        value_per_price_unit_per_lot=D("1"),
        volume_step=D("0.01"),
        minimum_volume=D("0.01"),
    )
    args.update(overrides)
    return calculate_position_size(**args)


def test_calculates_and_rounds_down():
    result = base()
    assert result.status == "PASS"
    assert result.risk_budget == D("100")
    assert result.recommended_volume == D("20.00")
    assert result.estimated_risk <= result.risk_budget


def test_missing_stop_is_not_zero_risk():
    result = base(stop_loss=None)
    assert result.status == "INSUFFICIENT_DATA"
    assert result.recommended_volume is None
    assert "required" in result.message


def test_minimum_volume_does_not_force_oversizing():
    result = base(equity=D("100"), risk_percent=D("0.1"), minimum_volume=D("0.1"))
    assert result.status == "WARNING"
    assert result.recommended_volume is None


def test_invalid_zero_stop_distance_rejected():
    with pytest.raises(ValueError):
        base(stop_loss=D("100"))


def test_risk_budget_rejects_over_100_percent():
    with pytest.raises(ValueError):
        base(risk_percent=D("101"))


def test_lower_risk_budget_never_increases_size():
    higher = base(risk_percent=D("2"))
    lower = base(risk_percent=D("1"))
    assert higher.recommended_volume is not None
    assert lower.recommended_volume is not None
    assert lower.recommended_volume <= higher.recommended_volume
