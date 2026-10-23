# Development Setup

## Prerequisites
- Python 3.11 or newer.
- Git.
- Node.js LTS will be required when the web application scaffold is added.
- PostgreSQL will be required when persistence is introduced.

## Run the risk engine tests
From the repository root:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -e "packages/risk_engine[dev]"
python -m pytest packages/risk_engine/tests -q
```

## Run the API locally
```bash
python -m pip install -r services/api/requirements.txt
cd services/api
uvicorn app.main:app --reload
```

Health endpoint: `http://127.0.0.1:8000/health`
OpenAPI docs: `http://127.0.0.1:8000/docs`

The current API is only a foundation. Authentication, persistence, and account endpoints are not implemented yet. Do not expose it publicly or connect real accounts at this stage.
