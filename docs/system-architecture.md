# System Architecture

## High-level flow
Browser (Next.js) → FastAPI API → application services/repositories → PostgreSQL.
The standalone risk engine is imported by backend services and can be tested independently. The MT5 connector sends authenticated, validated, read-only snapshots to a dedicated ingestion endpoint.

## Trust boundaries
- Browser sessions and API authentication.
- API service and database.
- MT5 terminal connector and ingestion endpoint.
- External market/broker metadata and currency conversion inputs.

## Rules
- No broker trading password is requested or stored.
- Connector pairing uses short-lived, single-use codes and revocable scoped credentials.
- All ingestion payloads include schema version, account reference, event ID, and UTC timestamp.
- Reject malformed, duplicate, stale, or implausible payloads with explicit status.
- All account-scoped operations enforce user ownership server-side.
- Risk calculations require verified instrument metadata and conversion assumptions.
- AI can explain already-computed results, but cannot invent calculation inputs or bypass policy rules.

## Implementation order
1. Repository and docs.
2. Standalone risk engine with unit/property tests.
3. API schemas, persistence, auth, and ownership checks.
4. Demo data and read-only ingestion protocol.
5. Frontend dashboard and calculator.
6. MT5 terminal validation, security review, deployment.
