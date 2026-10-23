"""Portfolio-level risk and data freshness calculations.

All money values must already be converted to the account's base currency by a
trusted adapter. This module deliberately does not guess missing broker metadata.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from typing import Iterable, Optional


@dataclass(frozen=True)
class PositionRisk:
    symbol: str
    market_value: Decimal
    stop_risk: Optional[Decimal]
    sector: Optional[str] = None


@dataclass(frozen=True)
class PortfolioRiskResult:
    status: str
    gross_exposure: Decimal
    exposure_percent: Optional[Decimal]
    known_stop_risk: Decimal
    known_stop_risk_percent: Optional[Decimal]
    unbounded_positions: int
    largest_symbol: Optional[str]
    concentration_percent: Optional[Decimal]
    warnings: tuple[str, ...]


def analyse_portfolio(*, equity: Decimal, positions: Iterable[PositionRisk],
                      concentration_limit_percent: Decimal = Decimal("10")) -> PortfolioRiskResult:
    """Summarise gross exposure and stop-defined risk without hiding unknown risk."""
    if not equity.is_finite() or equity <= 0:
        raise ValueError("equity must be finite and positive")
    if not concentration_limit_percent.is_finite() or concentration_limit_percent <= 0:
        raise ValueError("concentration_limit_percent must be finite and positive")
    items = tuple(positions)
    for item in items:
        if not item.market_value.is_finite() or item.market_value < 0:
            raise ValueError("market_value must be finite and non-negative")
        if item.stop_risk is not None and (not item.stop_risk.is_finite() or item.stop_risk < 0):
            raise ValueError("stop_risk must be finite and non-negative")
    gross = sum((p.market_value for p in items), Decimal("0"))
    known_risk = sum((p.stop_risk for p in items if p.stop_risk is not None), Decimal("0"))
    unbounded = sum(p.stop_risk is None for p in items)
    symbol_totals: dict[str, Decimal] = {}
    for p in items:
        symbol_totals[p.symbol] = symbol_totals.get(p.symbol, Decimal("0")) + p.market_value
    largest = max(symbol_totals, key=symbol_totals.get) if symbol_totals else None
    concentration = symbol_totals[largest] / equity * 100 if largest else None
    warnings = []
    if unbounded:
        warnings.append(f"{unbounded} position(s) have unknown stop-based risk because stop-loss data is missing.")
    if concentration is not None and concentration > concentration_limit_percent:
        warnings.append(f"Largest symbol exposure exceeds the {concentration_limit_percent}% concentration threshold.")
    if gross / equity * 100 > 100:
        warnings.append("Gross exposure exceeds account equity; review leverage and margin.")
    return PortfolioRiskResult(
        "WARNING" if warnings else "PASS", gross, gross / equity * 100,
        known_risk, known_risk / equity * 100, unbounded, largest, concentration,
        tuple(warnings),
    )


def maximum_drawdown_percent(equity_curve: Iterable[Decimal]) -> Decimal:
    """Return peak-to-trough drawdown percentage (positive magnitude)."""
    values = tuple(equity_curve)
    if not values:
        raise ValueError("equity_curve cannot be empty")
    if any(not x.is_finite() or x <= 0 for x in values):
        raise ValueError("equity values must be finite and positive")
    peak = values[0]
    worst = Decimal("0")
    for value in values:
        peak = max(peak, value)
        worst = max(worst, (peak - value) / peak * 100)
    return worst


def data_freshness(*, observed_at: datetime, now: Optional[datetime] = None,
                   stale_after_seconds: int = 60) -> tuple[str, int]:
    """Return (FRESH|STALE, age seconds); naive timestamps are rejected."""
    current = now or datetime.now(timezone.utc)
    if observed_at.tzinfo is None or current.tzinfo is None:
        raise ValueError("observed_at and now must be timezone-aware")
    if stale_after_seconds < 0:
        raise ValueError("stale_after_seconds cannot be negative")
    age = max(0, int((current - observed_at).total_seconds()))
    return ("STALE" if age > stale_after_seconds else "FRESH", age)
