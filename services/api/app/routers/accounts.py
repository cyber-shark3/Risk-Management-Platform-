"""User-owned accounts and read-only positions."""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from ..database import get_db
from ..dependencies import get_current_user
from ..models import Position, TradingAccount, User
from ..schemas import AccountCreate, AccountPublic, PositionPublic

router = APIRouter(tags=["accounts"])


@router.get("/accounts", response_model=list[AccountPublic])
def list_accounts(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return list(db.scalars(select(TradingAccount).where(TradingAccount.owner_id == user.id).order_by(TradingAccount.id.desc())))


@router.post("/accounts", response_model=AccountPublic, status_code=status.HTTP_201_CREATED)
def create_account(payload: AccountCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    account = TradingAccount(
        owner_id=user.id, label=payload.label.strip(), broker=payload.broker.strip(),
        platform=payload.platform, currency=payload.currency.upper(),
        equity=payload.equity, balance=payload.balance, observed_at=datetime.now(timezone.utc),
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@router.get("/accounts/{account_id}/positions", response_model=list[PositionPublic])
def list_positions(account_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    account = db.scalar(
        select(TradingAccount).options(selectinload(TradingAccount.positions))
        .where(TradingAccount.id == account_id, TradingAccount.owner_id == user.id)
    )
    if account is None:
        # Same response for missing and foreign-owned accounts to avoid account enumeration.
        raise HTTPException(status_code=404, detail="Account not found")
    return account.positions


@router.get("/positions", response_model=list[PositionPublic])
def list_all_positions(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return list(db.scalars(
        select(Position).join(TradingAccount)
        .where(TradingAccount.owner_id == user.id).order_by(Position.id.desc())
    ))
