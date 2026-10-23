"""Minimal API foundation. Business endpoints will be added behind explicit auth."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CI × Nasara Risk Management Platform API",
    version="0.1.0",
    description=(
        "Read-only trading risk intelligence API. No trade execution endpoints are exposed."
    ),
)

# Local development defaults only. Production origins must be configured explicitly.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
)


@app.get("/health", tags=["operations"])
def health() -> dict[str, str]:
    """Basic process health check; does not imply database or broker connectivity."""
    return {"status": "ok", "service": "risk-platform-api", "version": "0.1.0"}


@app.get("/api/v1", tags=["operations"])
def api_root() -> dict[str, str]:
    """API discovery endpoint."""
    return {
        "name": "CI × Nasara Risk Management Platform",
        "version": "0.1.0",
        "mode": "read-only",
        "trading_execution": "disabled",
    }
