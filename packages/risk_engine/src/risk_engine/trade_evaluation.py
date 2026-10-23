"""Rule-based trade risk evaluation; this is not a profitability prediction."""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from .position_sizing import calculate_position_size


@dataclass(frozen=True)
class TradeEvaluation:
    status: str
    risk_budget: Decimal
    estimated_risk: Optional[Decimal]
    risk_percent_of_equity: Optional[Decimal]
    recommended_volume: Optional[Decimal]
    reasons: tuple[str, ...]


def evaluate_trade(*, equity: Decimal, risk_percent: Decimal, entry_price: Decimal,
                   stop_loss: Optional[Decimal], value_per_price_unit_per_lot: Decimal,
                   volume_step: Decimal, minimum_volume: Decimal,
                   maximum_volume: Optional[Decimal] = None,
                   existing_stop_risk: Decimal = Decimal("0"),
                   portfolio_risk_limit_percent: Decimal = Decimal("5")) -> TradeEvaluation:
    """Evaluate a hypothetical position against a budget and a total-risk limit."""
    if not existing_stop_risk.is_finite() or existing_stop_risk < 0:
        raise ValueError("existing_stop_risk must be finite and non-negative")
    if not portfolio_risk_limit_percent.is_finite() or portfolio_risk_limit_percent <= 0:
        raise ValueError("portfolio_risk_limit_percent must be finite and positive")
    sized = calculate_position_size(
        equity=equity, risk_percent=risk_percent, entry_price=entry_price,
        stop_loss=stop_loss, value_per_price_unit_per_lot=value_per_price_unit_per_lot,
        volume_step=volume_step, minimum_volume=minimum_volume, maximum_volume=maximum_volume,
    )
    reasons = [sized.message]
    if sized.recommended_volume is None or sized.estimated_risk is None:
        return TradeEvaluation(sized.status, sized.risk_budget, None, None, None, tuple(reasons))
    total_risk = existing_stop_risk + sized.estimated_risk
    total_pct = total_risk / equity * 100
    if total_pct > portfolio_risk_limit_percent:
        reasons.append(f"Combined known stop risk would exceed the {portfolio_risk_limit_percent}% portfolio limit.")
        return TradeEvaluation("BLOCK", sized.risk_budget, sized.estimated_risk, total_pct,
                               None, tuple(reasons))
    return TradeEvaluation("PASS", sized.risk_budget, sized.estimated_risk, total_pct,
                           sized.recommended_volume, tuple(reasons))
