"""Validated public API schemas."""
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)

    @field_validator("password")
    @classmethod
    def reject_common_empty_passwords(cls, value: str) -> str:
        if value.strip() != value or not any(ch.isalpha() for ch in value) or not any(ch.isdigit() for ch in value):
            raise ValueError("Password must contain letters and numbers and have no leading/trailing spaces")
        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class AccountCreate(BaseModel):
    label: str = Field(min_length=1, max_length=100)
    broker: str = Field(default="Manual", max_length=100)
    platform: str = Field(default="MT5", pattern="^(MT5|MT4|MANUAL)$")
    currency: str = Field(default="USD", min_length=3, max_length=3)
    equity: Decimal = Field(ge=0, max_digits=18, decimal_places=2)
    balance: Decimal = Field(ge=0, max_digits=18, decimal_places=2)


class AccountPublic(BaseModel):
    id: int
    label: str
    broker: str
    platform: str
    currency: str
    equity: Decimal
    balance: Decimal
    observed_at: datetime | None


class PositionPublic(BaseModel):
    id: int
    account_id: int
    symbol: str
    side: str
    volume: Decimal
    entry_price: Decimal
    current_price: Decimal | None
    stop_loss: Decimal | None
    unrealised_pnl: Decimal | None
    observed_at: datetime | None


class PositionSizeRequest(BaseModel):
    equity: Decimal = Field(gt=0)
    risk_percent: Decimal = Field(gt=0, le=100)
    entry_price: Decimal = Field(gt=0)
    stop_loss: Decimal | None = None
    value_per_price_unit_per_lot: Decimal = Field(gt=0)
    volume_step: Decimal = Field(gt=0)
    minimum_volume: Decimal = Field(gt=0)
    maximum_volume: Decimal | None = Field(default=None, gt=0)


class TradeEvaluationRequest(PositionSizeRequest):
    existing_stop_risk: Decimal = Field(default=Decimal("0"), ge=0)
    portfolio_risk_limit_percent: Decimal = Field(default=Decimal("5"), gt=0)
