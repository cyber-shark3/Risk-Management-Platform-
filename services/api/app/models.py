"""Persistence models. Broker passwords and trading credentials are intentionally absent."""
from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(512), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    accounts: Mapped[list["TradingAccount"]] = relationship(back_populates="owner", cascade="all, delete-orphan")


class TradingAccount(Base):
    __tablename__ = "trading_accounts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    broker: Mapped[str] = mapped_column(String(100), default="Manual", nullable=False)
    platform: Mapped[str] = mapped_column(String(20), default="MT5", nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    equity: Mapped[float] = mapped_column(Numeric(18, 2), default=0, nullable=False)
    balance: Mapped[float] = mapped_column(Numeric(18, 2), default=0, nullable=False)
    observed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    owner: Mapped[User] = relationship(back_populates="accounts")
    positions: Mapped[list["Position"]] = relationship(back_populates="account", cascade="all, delete-orphan")


class Position(Base):
    __tablename__ = "positions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("trading_accounts.id", ondelete="CASCADE"), index=True, nullable=False)
    symbol: Mapped[str] = mapped_column(String(40), nullable=False)
    side: Mapped[str] = mapped_column(String(5), nullable=False)
    volume: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False)
    entry_price: Mapped[float] = mapped_column(Numeric(18, 8), nullable=False)
    current_price: Mapped[float | None] = mapped_column(Numeric(18, 8), nullable=True)
    stop_loss: Mapped[float | None] = mapped_column(Numeric(18, 8), nullable=True)
    unrealised_pnl: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    observed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    account: Mapped[TradingAccount] = relationship(back_populates="positions")
