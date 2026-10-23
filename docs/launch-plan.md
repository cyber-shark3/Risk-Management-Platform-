# Pilot Launch Plan — November 2026

**Product:** COLLECTION INDUSTRIES × NASARA INVESTMENTS Risk Management Platform  
**Plan date:** 23 October 2026  
**Target:** Private pilot with the first 10 clients, followed by a public-launch decision only after acceptance checks pass.  
**Commercial model:** Free controlled pilot, then freemium with any paid prices stated in NAD (N$).  
**Budget envelope:** N$500–N$2,000; confirm actual spend before purchasing services.

## Product decisions already agreed
- Target retail and professional traders.
- Initial account inputs: manual entry and MetaTrader 5 (MT5).
- Initial features: position sizing, account monitoring, portfolio exposure, drawdown monitoring, trade evaluation, risk-limit warnings and an AI assistant that explains results.
- Dashboard includes equity/balance, open positions, known stop risk, exposure, current/maximum drawdown, warnings, recent activity, position calculator and trade evaluation.
- Branding: COLLECTION INDUSTRIES × NASARA INVESTMENTS.
- Visual direction: dark navy and white, restrained blue accents, readable charts and clear warning states.
- Private pilot before public registration.
- No trade execution in the initial product.

## Milestones and acceptance gates

### 23–25 October — Scope and release controls
- [x] Record product and pilot decisions in product requirements.
- [ ] Confirm whether an MT5 demo account is available.
- [ ] Choose temporary deployment URL or domain.
- [ ] Confirm target date: pilot by 23 November, public launch decision by 30 November.
- [ ] Confirm approved logos and brand assets.
- [ ] Freeze first-release scope; defer nonessential features.

**Gate:** No secrets, broker passwords or live trading credentials are to be shared in chat or committed to the repository.

### 26 October–1 November — Risk engine and persistence
- [ ] Test all risk formulas against independent examples.
- [ ] Validate volume-step/minimum-lot and missing-stop cases.
- [ ] Add database migrations rather than relying on create-all in production.
- [ ] Add persistent risk policies, alert records and account activity/audit events.
- [ ] Verify account ownership checks for every user-owned endpoint.
- [ ] Confirm NAD is displayed as the platform's commercial currency, while each trading account retains its own actual account currency.

**Gate:** No broker-specific stop-risk figure is presented as reliable until contract/tick values and currency conversions are validated.

### 2–8 November — Dashboard and account workflows
- [ ] Complete responsive dashboard layout and brand presentation.
- [ ] Wire dashboard cards to API data rather than illustrative values.
- [ ] Clearly label manual, simulated and connector-sourced data.
- [ ] Implement position calculator and trade evaluation workspace.
- [ ] Implement explainable risk warnings and recent activity.
- [ ] Add clear empty/loading/error states and stale-data indicators.

**Gate:** Manual account data can be created, retrieved and reflected accurately in the dashboard after restarting the services.

### 9–15 November — MT5 demo ingestion and monitoring
- [ ] Choose connector architecture and threat model.
- [ ] Implement read-only ingestion with authenticated pairing and revocation.
- [ ] Test demo account snapshots, positions, timestamps and duplicate/replayed events.
- [ ] Validate broker-specific symbol specifications, tick/contract values, lot steps and account currency.
- [ ] Add failure, offline and stale-data alerts.

**Gate:** Do not describe MT5 as integrated until a complete demo data flow has been tested end to end. Never request/store broker trading passwords.

### 16–22 November — Private pilot readiness
- [ ] Run automated unit/API and end-to-end tests.
- [ ] Test isolation between two users and account ownership enforcement.
- [ ] Review password policy, token/session controls, rate limits, CORS, secrets and HTTPS.
- [ ] Test database backup and restore.
- [ ] Verify monitoring, error logs, support contact and incident response.
- [ ] Recruit up to 10 pilot users and collect structured feedback.
- [ ] Document known limitations and obtain appropriate user consent.

**Gate:** No pilot with real account data until security and data handling have been reviewed. Start with demo/manual data where possible.

### 23–30 November — Pilot and release decision
- [ ] Fix all critical/high-severity defects discovered in the pilot.
- [ ] Review feedback, usability and calculation correctness.
- [ ] Confirm hosting, domain, email, backup and monitoring costs against budget.
- [ ] Review applicable Namibian and target-market legal, data-protection and financial-services requirements.
- [ ] Decide whether public launch is justified; extend the private pilot if any critical gate remains open.

## Definition of pilot-ready
- Core calculations pass tests and have documented assumptions.
- Missing stop loss or missing instrument data is shown as unknown/insufficient, never zero risk.
- Volume is rounded down and minimum-lot oversizing is rejected.
- Stale or offline data is visible.
- Dashboard uses actual API results and labels sample data.
- User accounts and records are properly isolated.
- Backup/restore, HTTPS, secrets and operational monitoring are checked.
- Manual/demo workflow works end to end.
- MT5 integration is labelled unavailable until it has passed a real demo end-to-end test.
- Support, limitations and incident handling are documented.

## Decisions still needed from product owner
1. MT5 demo account available: yes / no / use simulated data for now.
2. Domain: existing domain / choose one / temporary URL first.
3. Release target: pilot by 23 November / public launch by 30 November if gates pass / different date.
4. Approved logos and brand assets.
5. Final free-tier limits, paid-tier features and NAD pricing (after pilot feedback).

## Operating principle
A date is a target, not permission to bypass financial-accuracy, privacy, security or legal checks. If a release gate fails, keep the product in private testing and state the limitation honestly.
