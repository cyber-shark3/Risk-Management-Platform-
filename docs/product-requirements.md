# Product Requirements

## Product and ownership
**Product:** COLLECTION INDUSTRIES × NASARA INVESTMENTS Risk Management Platform  
**Launch strategy:** Private pilot with the first 10 clients.  
**Commercial model:** Freemium after the initial pilot; prices and paid features are to be stated in Namibian dollars (NAD/N$). No prices are final until approved by the owners.  
**Initial audience:** Retail and professional traders (with a path to investment-firm features later).

## Supported account input
- Manual account entry and clearly labelled sample/demo data are available for development and pilot testing.
- MetaTrader 5 (MT5) is the target broker-data integration for the initial release.
- MT5 integration must be read-only. It must not place, modify, or close trades.
- MT4 and other platforms are out of scope until MT5 ingestion, accuracy and safety checks are stable.
- Never request or store a user's broker trading password.

## MVP launch features
1. Position-size calculator using equity, risk percentage, entry, stop loss, broker-specific value per price unit per lot, volume step and minimum/maximum volume.
2. Account monitoring for balance, equity, margin where supplied, open positions and last successful update.
3. Portfolio exposure reporting, with assumptions and data limitations clearly shown.
4. Current and maximum drawdown monitoring.
5. Trade evaluation against configured risk rules, returning PASS, WARNING, FAIL or INSUFFICIENT_DATA.
6. Risk-limit warnings and alerts, with an explanation of the trigger.
7. AI risk assistant to explain existing calculations and reports in plain language. AI must not invent market/broker data, override deterministic calculations or promise profitable trades.

## Required dashboard
- Account equity and balance.
- Current open positions.
- Known stop-based risk, clearly distinguishing unknown/unbounded risk when a stop loss or required instrument data is missing.
- Portfolio exposure.
- Current and maximum drawdown.
- Risk-limit warnings.
- Recent account activity.
- Position-size calculator.
- Trade-evaluation workspace.
- Clear COLLECTION INDUSTRIES × NASARA INVESTMENTS branding.
- Responsive mobile and desktop layouts. Preferred visual direction: dark navy and white, restrained blue accents, readable charts and clear warning colours. This is the initial design direction and can be adjusted after review.

## Initial pilot and pricing
- First 10 pilot clients are invited for controlled testing; the pilot is not a promise of production-grade service.
- After the pilot, use a freemium model: a free entry tier and optional paid features.
- All proposed prices and subscription communications must use NAD/N$. The actual prices, tier limits and billing provider remain to be approved.
- Start with a private pilot before opening public registration.

## Risk and data-quality rules
- Show whether data is sample, manually entered or received from an MT5 connector.
- Show the last successful update and stale/offline state.
- Explain why a check passed, warned or failed.
- Missing required inputs produce INSUFFICIENT_DATA, never an invented zero.
- A position without a stop loss has unknown/unbounded stop-based risk; do not report it as zero.
- Validate broker-specific contract size, tick value, volume step, account currency and conversion rates before presenting stop-based risk as reliable.
- Round recommended volume down to the broker's volume step. Never round up to the minimum lot if that would exceed the risk budget.
- A PASS means only that configured checks passed; it does not mean a trade is profitable.
- Clearly disclose assumptions, fees/slippage/gap exclusions and stale or incomplete data.

## Out of scope for initial release
- Placing, modifying or closing trades.
- Guaranteed trade signals, guaranteed profits or personalised investment promises.
- Copy trading, autonomous execution and leverage recommendations.
- MT4 integration.
- Treating illustrative chart data as a user's real performance.

## Security and release requirements
- Authentication and ownership checks on every user-owned resource.
- Secure password hashing, strong secret management, rate limiting and appropriate session/token controls.
- No secrets committed to source control.
- HTTPS for public deployment.
- Audit logging for important account, policy and connector events.
- Documented backup, restore and incident-response procedures.
- Review applicable Namibian and target-market legal, data-protection and financial-services requirements before public launch.
- Do not claim certification or regulatory compliance without independent verification.

## Pilot acceptance criteria
- Financial calculations are tested against independently calculated examples and validated instrument specifications.
- Automated tests cover missing stops, stale data, minimum-lot edge cases, volume-step rounding, drawdown, ownership checks and risk-limit outcomes.
- The complete manual/demo account workflow works from data entry through the dashboard and risk evaluation.
- MT5 demo ingestion is tested end to end before it is described as available.
- A small pilot group has tested mobile and desktop flows.
- Known limitations are visible and support/incident handling is documented.
- A pilot release is not considered public-production readiness until deployment, security, backup/restore and operational checks are complete.
