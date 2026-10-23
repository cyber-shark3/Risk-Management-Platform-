# COLLECTION INDUSTRIES × NASARA INVESTMENTS
## Retail Trader Risk Intelligence Platform

A read-only risk-intelligence platform designed to help retail traders understand exposure, position sizing, data freshness and portfolio risk. **It does not place, modify, or close trades.** It does not promise profitable outcomes.

## Implemented in feature branch

- Deterministic Python risk engine using Decimal: conservative position sizing, portfolio gross exposure, unknown stop-risk detection, drawdown, stale-data checks and portfolio-aware trade evaluation.
- FastAPI with registration, Argon2 password hashing, short-lived signed bearer tokens, authenticated user profile, owner-scoped account/position reads, manual account snapshot creation, dashboard summary and risk calculation endpoints.
- SQLAlchemy persistence models for users, trading accounts and positions. Local SQLite is supported for quick development; PostgreSQL is configured for Compose.
- Next.js/TypeScript responsive dashboard with sign-in/register, summary cards, data-quality warnings, account list and manual account snapshots.
- Unit/API tests and GitHub Actions CI.
- Docker Compose local development setup.

## Local development

Prerequisites: Docker Desktop, or Python 3.12 and Node.js 22.

1. Copy `services/api/.env.example` to `services/api/.env` and set a long random `SECRET_KEY`. For Compose, set `SECRET_KEY` and `POSTGRES_PASSWORD` in a root `.env` file.
2. From the repository root run `docker compose up --build`.
3. Open the dashboard at `http://localhost:3000`; API documentation at `http://localhost:8000/docs`.
4. Register with a password of at least 12 characters containing letters and numbers. Add a manual account snapshot to populate the account list.

### Tests without Docker

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -e "packages/risk_engine[dev]"
python -m pip install -r services/api/requirements.txt
PYTHONPATH=packages/risk_engine/src:services/api python -m pytest packages/risk_engine/tests services/api/tests -q
```

## API routes

- `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `GET /api/v1/auth/me`
- `GET/POST /api/v1/accounts`, `GET /api/v1/accounts/{id}/positions`, `GET /api/v1/positions`
- `GET /api/v1/dashboard/summary`
- `POST /api/v1/risk/position-size`, `POST /api/v1/risk/evaluate`
- `GET /health`

## Important limitations

This is an early-stage foundation, **not a production-certified financial or security product**. CI/test execution and a deployed runtime have not yet been verified for this branch. Before public launch, add Alembic migrations, account recovery/email verification, rate limiting and abuse controls, session revocation, security review, backup/restore drills, monitoring, secrets management and HTTPS.

The chart in the UI is illustrative sample data and is not sourced from your account. Manual snapshots do not connect to a broker. There is no MT5 bridge yet. No broker passwords are requested or stored. Do not report stop-based position risk as known until broker-specific contract/tick values and currency conversions are validated. Missing stops or stale data are warnings, not zero risk. Keep live broker integration read-only until separately reviewed.
