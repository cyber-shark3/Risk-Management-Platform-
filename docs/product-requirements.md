# Product Requirements

## Users
Retail traders who want to understand account-level and proposed-trade risk before making their own decisions.

## MVP
- Demo account with clearly labelled sample data.
- Account overview: balance, equity, margin, open risk, drawdown, last update.
- Position list with direction, size, entry, current price, stop loss, take profit, and risk status.
- Position-size calculator based on account equity, risk percentage, entry, stop loss, and broker-specific value per price unit per lot.
- Trade-policy checks with PASS, WARNING, FAIL, or INSUFFICIENT_DATA outcomes.
- Risk policies for per-trade risk, daily loss, drawdown, and exposure.
- Read-only MT5 account snapshot ingestion after the demo experience is tested.
- Audit trail for important changes and connector events.

## Out of scope for MVP
- Placing, modifying, or closing trades.
- Guaranteed trade signals, guaranteed profits, or personalised investment promises.
- Copy trading, leverage recommendations, and autonomous execution.
- MT4 until MT5 protocol and safety checks are stable.

## UX rules
- Show whether data is demo or connected-account data.
- Show last successful update and stale/offline state.
- Explain why a check passed, warned, or failed.
- Missing inputs produce INSUFFICIENT_DATA, never an invented zero.
- A PASS means configured checks passed; it does not mean a trade is profitable.
