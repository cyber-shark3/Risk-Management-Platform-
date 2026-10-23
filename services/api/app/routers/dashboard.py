"""Dashboard summary and deterministic risk calculations."""
from datetime import datetime, timezone
from decimal import Decimal
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from risk_engine import PositionRisk, analyse_portfolio, calculate_position_size, evaluate_trade
from ..database import get_db
from ..dependencies import get_current_user
from ..models import Position, TradingAccount, User
from ..schemas import PositionSizeRequest, TradeEvaluationRequest

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard/summary")
def dashboard_summary(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    accounts = list(db.scalars(select(TradingAccount).where(TradingAccount.owner_id == user.id)))
    account_ids = [a.id for a in accounts]
    positions = list(db.scalars(select(Position).where(Position.account_id.in_(account_ids)))) if account_ids else []
    equity = sum((Decimal(a.equity) for a in accounts), Decimal("0"))
    balance = sum((Decimal(a.balance) for a in accounts), Decimal("0"))
    pnl_values = [Decimal(p.unrealised_pnl) for p in positions if p.unrealised_pnl is not None]
    missing_pnl = sum(p.unrealised_pnl is None for p in positions)
    risk_positions = []
    for p in positions:
        account = next((a for a in accounts if a.id == p.account_id), None)
        if account is None:
            continue
        market_value = abs(Decimal(p.volume) * Decimal(p.current_price or p.entry_price))
        stop_risk = None
        # This conservative approximation is explicitly not broker-contract-accurate.
        # Until validated tick/contract metadata is available, don't invent risk numbers.
        risk_positions.append(PositionRisk(p.symbol, market_value, stop_risk))
    portfolio = analyse_portfolio(equity=equity, positions=risk_positions) if equity > 0 else None
    latest = max((a.observed_at for a in accounts if a.observed_at), default=None)
    age = int((datetime.now(timezone.utc) - latest.replace(tzinfo=timezone.utc) if latest.tzinfo is None else datetime.now(timezone.utc) - latest).total_seconds()) if latest else None
    stale = age is None or age > 60
    warnings = []
    if not accounts:
        warnings.append("No trading accounts connected. Add a manual account or pair the MT5 connector later.")
    if stale:
        warnings.append("Account snapshot is missing or older than 60 seconds; live risk figures are unavailable.")
    if missing_pnl:
        warnings.append(f"P&L is unavailable for {missing_pnl} position(s).")
    if positions:
        warnings.append("Broker contract specifications and converted stop risk are not yet validated; position risk is unknown.")
    return {
        "account_count": len(accounts), "position_count": len(positions),
        "equity": str(equity), "balance": str(balance),
        "unrealised_pnl": str(sum(pnl_values, Decimal("0"))) if len(pnl_values) == len(positions) else None,
        "known_stop_risk": "0" if not positions else None,
        "gross_exposure": str(portfolio.gross_exposure) if portfolio else None,
        "exposure_percent": str(portfolio.exposure_percent) if portfolio and portfolio.exposure_percent is not None else None,
        "data_status": "STALE" if stale else "FRESH", "last_snapshot_at": latest.isoformat() if latest else None,
        "warnings": warnings,
        "mode": "read-only", "trading_execution": "disabled",
    }


@router.post("/risk/position-size")
def position_size(payload: PositionSizeRequest, user: User = Depends(get_current_user)):
    result = calculate_position_size(**payload.model_dump())
    return {
        "status": result.status, "risk_budget": str(result.risk_budget),
        "stop_distance": str(result.stop_distance) if result.stop_distance is not None else None,
        "raw_volume": str(result.raw_volume) if result.raw_volume is not None else None,
        "recommended_volume": str(result.recommended_volume) if result.recommended_volume is not None else None,
        "estimated_risk": str(result.estimated_risk) if result.estimated_risk is not None else None,
        "message": result.message,
    }


@router.post("/risk/evaluate")
def evaluate(payload: TradeEvaluationRequest, user: User = Depends(get_current_user)):
    result = evaluate_trade(**payload.model_dump())
    return {
        "status": result.status, "risk_budget": str(result.risk_budget),
        "estimated_risk": str(result.estimated_risk) if result.estimated_risk is not None else None,
        "risk_percent_of_equity": str(result.risk_percent_of_equity) if result.risk_percent_of_equity is not None else None,
        "recommended_volume": str(result.recommended_volume) if result.recommended_volume is not None else None,
        "reasons": list(result.reasons),
    }
