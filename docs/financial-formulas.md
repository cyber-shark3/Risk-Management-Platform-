# Financial Formula Notes

All formulas must document assumptions and currency units. Do not silently substitute zero for missing values.

## Risk budget
risk_budget = account_equity × (risk_percent / 100)

## Stop distance
stop_distance = abs(entry_price − stop_loss_price)
A missing stop loss means stop-based risk is UNKNOWN / UNBOUNDED, not zero.

## Position size
For a broker-validated instrument where `value_per_price_unit_per_lot` is the account-currency value of a one-price-unit move for one lot:

raw_lots = risk_budget / (stop_distance × value_per_price_unit_per_lot)

rounded_lots = floor(raw_lots / volume_step) × volume_step

The instrument value must account for contract size, tick size/value, account currency, and conversion rate. This simplified formula must not be used unless that input is correctly derived for the instrument and account.

If rounded size is below broker minimum volume, return no recommended size and explain that minimum volume exceeds the risk budget. Never round up above the risk budget.

## Risk/reward
For a long position: reward distance = take_profit − entry; risk distance = entry − stop.
For a short position: reward distance = entry − take_profit; risk distance = stop − entry.
Both distances must be positive and directionally valid. Exclude fees/slippage unless explicitly modelled; disclose the limitation.

## Drawdown
peak_equity = maximum equity observed to date
drawdown_amount = peak_equity − current_equity
drawdown_percent = drawdown_amount / peak_equity × 100, only when peak_equity > 0.

## Undefined results
Profit factor with zero gross losses, ratios with zero denominators, missing history, stale quotes, and missing conversion rates must be represented explicitly as undefined/insufficient data—not zero.
