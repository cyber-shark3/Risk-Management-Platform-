# Initial Threat Model

## Assets
User identity and sessions, account snapshots, trading history, risk policies, connector credentials, audit events, deployment secrets.

## Main threats
- Account data exposure across users.
- Theft or replay of connector credentials.
- Forged or duplicated connector events.
- Injection through malformed payloads.
- Secrets leaking into logs or Git.
- Incorrect risk calculations caused by bad instrument metadata or currency conversion.
- Stale data displayed as current.
- Excessive API requests and denial of service.

## Minimum controls
- Strong password hashing and secure session handling.
- Server-side authorization for every account-scoped operation.
- Short-lived pairing code; scoped revocable connector token; hashed token storage.
- HTTPS in deployed environments, request validation, rate limits, and replay/idempotency checks.
- Redact secrets and personal/account data from logs.
- Keep secrets in environment/secret manager; rotate compromised credentials.
- Show timestamps and stale status; fail closed on missing critical calculation inputs.
- Backups, retention/deletion process, dependency scanning, and incident response plan.

This is an initial checklist, not a completed security assessment or compliance certification.
