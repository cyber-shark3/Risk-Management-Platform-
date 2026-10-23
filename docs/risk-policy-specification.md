# Risk Policy Specification

Each policy has an owner, version, effective timestamp, and audit record. Policy evaluation is deterministic.

## Initial checks
- Required inputs and data freshness.
- Stop-loss presence and direction validity.
- Estimated risk per trade versus configured maximum.
- Aggregate open risk versus configured maximum.
- Daily loss versus configured limit.
- Current drawdown versus configured limit.
- Instrument and currency concentration.
- Margin information availability and broker constraints.
- Position size and volume-step constraints.

## Outcomes
- PASS: all configured checks with sufficient reliable data passed.
- WARNING: a non-blocking concern or a policy near its limit exists.
- FAIL: a configured hard limit or validity rule is breached.
- INSUFFICIENT_DATA: required values are missing, stale, inconsistent, or unverified.

A policy engine is decision support only. It must not say that a trade is safe or profitable. Every result includes check IDs, outcome, explanation, inputs used, and policy version.
