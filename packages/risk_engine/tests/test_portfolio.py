from datetime import datetime, timedelta, timezone
from decimal import Decimal as D

import pytest
from risk_engine import PositionRisk, analyse_portfolio, data_freshness, maximum_drawdown_percent


def test_missing_stop_is_counted_as_unknown_not_zero():
    result = analyse_portfolio(equity=D("10000"), positions=[
        PositionRisk("EURUSD", D("2000"), None),
        PositionRisk("GBPUSD", D("1000"), D("25")),
    ])
    assert result.unbounded_positions == 1
    assert result.known_stop_risk == D("25")
    assert result.status == "WARNING"
    assert result.warnings


def test_gross_exposure_and_concentration():
    result = analyse_portfolio(equity=D("10000"), positions=[
        PositionRisk("XAUUSD", D("1500"), D("20")),
        PositionRisk("XAUUSD", D("500"), D("10")),
    ])
    assert result.gross_exposure == D("2000")
    assert result.concentration_percent == D("20.0")
    assert result.status == "WARNING"


def test_maximum_drawdown():
    assert maximum_drawdown_percent([D("100"), D("120"), D("90"), D("110")]) == D("25")


def test_empty_drawdown_rejected():
    with pytest.raises(ValueError):
        maximum_drawdown_percent([])


def test_stale_data_flag():
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    assert data_freshness(observed_at=now-timedelta(seconds=61), now=now) == ("STALE", 61)
    assert data_freshness(observed_at=now-timedelta(seconds=10), now=now) == ("FRESH", 10)


def test_naive_timestamps_rejected():
    with pytest.raises(ValueError):
        data_freshness(observed_at=datetime(2026, 1, 1))
