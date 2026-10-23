from decimal import Decimal as D
from risk_engine import evaluate_trade


def _evaluate(**overrides):
    values = dict(
        equity=D("10000"), risk_percent=D("1"), entry_price=D("100"),
        stop_loss=D("95"), value_per_price_unit_per_lot=D("1"),
        volume_step=D("0.01"), minimum_volume=D("0.01"),
        existing_stop_risk=D("400"), portfolio_risk_limit_percent=D("5"),
    )
    values.update(overrides)
    return evaluate_trade(**values)


def test_trade_passes_when_combined_risk_within_limit():
    result = _evaluate(existing_stop_risk=D("300"))
    assert result.status == "PASS"
    assert result.recommended_volume == D("20.00")
    assert result.risk_percent_of_equity == D("4.00")


def test_trade_blocked_when_combined_risk_exceeds_limit():
    result = _evaluate(existing_stop_risk=D("450"))
    assert result.status == "BLOCK"
    assert result.recommended_volume is None


def test_missing_stop_does_not_recommend_size():
    result = _evaluate(stop_loss=None)
    assert result.status == "INSUFFICIENT_DATA"
    assert result.recommended_volume is None
