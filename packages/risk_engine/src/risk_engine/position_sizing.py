"""Position sizing with Decimal arithmetic and conservative volume-step rounding.

The caller must supply a broker-validated account-currency value per price unit per lot.
This module does not derive contract specifications or currency conversions.
"""
from dataclasses import dataclass
from decimal import Decimal, ROUND_DOWN
from typing import Optional


@dataclass(frozen=True)
class PositionSizeResult:
    status: str
    risk_budget: Decimal
    stop_distance: Optional[Decimal]
    raw_volume: Optional[Decimal]
    recommended_volume: Optional[Decimal]
    estimated_risk: Optional[Decimal]
    message: str


def _positive(value: Decimal, field: str) -> None:
    if not value.is_finite() or value <= 0:
        raise ValueError(f"{field} must be a finite positive number")


def calculate_position_size(
    *,
    equity: Decimal,
    risk_percent: Decimal,
    entry_price: Decimal,
    stop_loss: Optional[Decimal],
    value_per_price_unit_per_lot: Decimal,
    volume_step: Decimal,
    minimum_volume: Decimal,
    maximum_volume: Optional[Decimal] = None,
) -> PositionSizeResult:
    """Calculate a conservative lot size for a stop-defined trade.

    A missing stop returns INSUFFICIENT_DATA; it is never interpreted as zero risk.
    The result rounds down to the broker's volume step and never rounds up to minimum
    volume when doing so would exceed the risk budget.
    """
    _positive(equity, "equity")
    _positive(risk_percent, "risk_percent")
    _positive(entry_price, "entry_price")
    _positive(value_per_price_unit_per_lot, "value_per_price_unit_per_lot")
    _positive(volume_step, "volume_step")
    _positive(minimum_volume, "minimum_volume")
    if risk_percent > Decimal("100"):
        raise ValueError("risk_percent cannot exceed 100")
    if maximum_volume is not None:
        _positive(maximum_volume, "maximum_volume")
        if maximum_volume < minimum_volume:
            raise ValueError("maximum_volume cannot be less than minimum_volume")

    budget = equity * risk_percent / Decimal("100")
    if stop_loss is None:
        return PositionSizeResult(
            "INSUFFICIENT_DATA", budget, None, None, None, None,
            "A stop loss is required to estimate stop-based risk.",
        )
    if not stop_loss.is_finite() or stop_loss <= 0:
        raise ValueError("stop_loss must be a finite positive number")

    distance = abs(entry_price - stop_loss)
    if distance == 0:
        raise ValueError("entry_price and stop_loss must differ")

    raw = budget / (distance * value_per_price_unit_per_lot)
    rounded = (raw / volume_step).to_integral_value(rounding=ROUND_DOWN) * volume_step
    if maximum_volume is not None:
        rounded = min(rounded, maximum_volume)
        rounded = (rounded / volume_step).to_integral_value(rounding=ROUND_DOWN) * volume_step

    if rounded < minimum_volume:
        return PositionSizeResult(
            "WARNING", budget, distance, raw, None, None,
            "The broker minimum volume exceeds the calculated risk budget; no size recommended.",
        )

    estimated = rounded * distance * value_per_price_unit_per_lot
    if estimated > budget:
        # Defensive guard: never return a size that exceeds the supplied risk budget.
        rounded = ((budget / (distance * value_per_price_unit_per_lot)) / volume_step) \
            .to_integral_value(rounding=ROUND_DOWN) * volume_step
        if rounded < minimum_volume:
            return PositionSizeResult(
                "WARNING", budget, distance, raw, None, None,
                "No broker-valid volume fits within the risk budget.",
            )
        estimated = rounded * distance * value_per_price_unit_per_lot

    return PositionSizeResult(
        "PASS", budget, distance, raw, rounded, estimated,
        "Estimated stop-based risk is within the requested budget, before fees, slippage, gaps, and conversion changes.",
    )
