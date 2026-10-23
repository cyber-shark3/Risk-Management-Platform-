"""Read-only CI × Nasara risk platform API."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import Base, engine
from . import models  # noqa: F401
from .routers import accounts, auth, dashboard

@asynccontextmanager
async def lifespan(_: FastAPI):
    # Convenience for local MVP. Production must use versioned Alembic migrations.
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title=settings.app_name, version="0.2.0",
    description="Read-only trading risk intelligence API. Trade execution is disabled.", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins, allow_credentials=True,
    allow_methods=["GET","POST","OPTIONS"], allow_headers=["Authorization","Content-Type","X-Request-ID"])
app.include_router(auth.router, prefix="/api/v1")
app.include_router(accounts.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")

@app.get("/health", tags=["operations"])
def health() -> dict[str,str]:
    return {"status":"ok","service":"risk-platform-api","version":"0.2.0"}

@app.get("/api/v1", tags=["operations"])
def api_root() -> dict[str,str]:
    return {"name":settings.app_name,"version":"0.2.0","mode":"read-only","trading_execution":"disabled"}
