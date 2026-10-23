# COLLECTION INDUSTRIES × NASARA INVESTMENTS
## Retail Trader Risk Intelligence Platform

A read-only risk-management and trading-decision-support platform for retail traders. The first release is designed to connect to MetaTrader 5 (MT5), ingest account and position information, and explain risk clearly. MT4 support is planned for a later phase.

> **Safety boundary:** This project does not place, modify, or close trades. It does not promise profitable trades or guaranteed predictions. Risk calculations depend on accurate broker instrument specifications, account currency conversions, and market data.

## Product goals
- Show account balance, equity, margin, open positions, and data freshness.
- Estimate position and portfolio risk using explicit, testable formulas.
- Help users calculate position size from a defined risk budget and stop-loss.
- Evaluate proposed trades against user-configured risk rules.
- Track drawdown, exposure, performance, and risk alerts.
- Start with a demo mode and a read-only MT5 connector.
- Keep calculations deterministic and auditable; AI may explain results but must never replace the calculation engine.

## Initial technology direction
- **Web:** Next.js, React, TypeScript, Tailwind CSS, Recharts.
- **API:** Python, FastAPI, Pydantic.
- **Data:** PostgreSQL, SQLAlchemy, Alembic.
- **Risk engine:** Python with decimal-safe money/price handling and explicit instrument metadata.
- **Quality:** pytest, Vitest/Playwright, lint/type checks, CI.
- **Operations:** Docker Compose for local development; secrets supplied through environment variables.

## Development principles
1. Correctness and transparent assumptions before features.
2. Read-only broker integration; never request or store broker trading passwords.
3. No fabricated live account data. Clearly label seeded examples as demo data.
4. Reject incomplete or stale data rather than silently producing confident results.
5. Enforce account ownership on every account-scoped API request.
6. Never describe a position without a stop-loss as zero-risk. Mark stop-based risk as unbounded/unknown.
7. Round position size down to the broker's volume step. If the minimum lot exceeds the risk budget, warn and do not recommend oversizing.
8. Store financial values with appropriate decimal precision and currency labels.
9. Tests must cover financial edge cases before live broker data is enabled.
10. No live trading execution in this project without a separate, explicit product and safety review.

## Repository layout
```text
apps/web/                 Next.js web application (planned)
services/api/             FastAPI application and API routes
packages/risk_engine/     Standalone deterministic risk calculations
integrations/mt5/         MT5 read-only connector (planned)
integrations/mt4/         Future MT4 connector (not in initial scope)
docs/                     Requirements, architecture, formulas, security
infrastructure/           Docker and deployment configuration (planned)
scripts/                  Development and validation helpers (planned)
tests/                    Contract and end-to-end tests (planned)
```

## Current implementation status
**Phase 1 — foundation started**
- Product requirements, architecture, financial formula notes, risk-policy rules, and initial threat model.
- Standalone Python position-sizing calculation using `Decimal`.
- Conservative volume-step rounding; missing stop-loss returns `INSUFFICIENT_DATA`; broker minimum volume never forces oversizing.
- Initial unit tests for position sizing and edge cases.
- Minimal FastAPI service with health and API discovery endpoints.
- GitHub Actions workflow for risk-engine tests and linting.

**Not implemented yet:** user authentication, database persistence, account ownership enforcement, dashboard, MT5 connector, alert delivery, full portfolio risk, and deployment. Do not expose this scaffold publicly or connect real trading accounts yet.

## Getting started
See [docs/development-setup.md](docs/development-setup.md). Never commit real credentials, account identifiers, customer data, or production secrets.
