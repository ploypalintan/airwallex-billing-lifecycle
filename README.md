# airwallex-billing-lifecycle

A small, runnable walkthrough of one subscription's lifecycle on Airwallex Billing, built in the sandbox with Python.

## Problem
Subscription businesses selling across currencies lose recurring revenue to failed renewals, not only to cancellations. Finance teams then struggle to see why a renewal failed, whether it recovered, and which payment settled which invoice. This repo follows one subscription through its billing lifecycle on Airwallex to see how much of that is visible and recoverable in one system.

## Who this is for
A mid-market subscription business in Asia selling in several currencies, with a finance team but no large engineering team. Outgrown a basic billing tool, but not at the scale where a heavy enterprise payments setup makes sense.

## Hypothesis
For this kind of business, one platform handling billing, payments and reconciliation should let a failed renewal be traced from invoice to payment attempt to retry to settlement through one ID chain, with no manual matching.

**Assumption to validate (not tested here):** that this buyer exists and feels this pain. That takes customer discovery, not a sandbox.

## Scope
**Built and tested:** customer, product, monthly price in a non-home currency, subscription via Billing Checkout, failed renewal, retry schedule, final UNPAID/CANCELLED state, webhooks, billing transactions (invoice to payment ID chain), one one-off invoice.

**Studied, not built:** usage-based billing, credit notes, tax, alternative payment methods.

## How I test it
1. Create a customer, product and monthly recurring price in a non-home currency.
2. Start a subscription through hosted Billing Checkout (AUTO_CHARGE).
3. Force a renewal to fail with a sandbox test card.
4. Record the retry schedule, final subscription status and webhook sequence.
5. Check whether the invoice links to a billing transaction, its Payment Intent and the payment attempt.
6. Create one one-off invoice.

## What this cannot show
The sandbox uses simulated money. It cannot prove approval-rate uplift or real recovery rates. It
cat > README.md <<'EOF'
# airwallex-billing-lifecycle

A small, runnable walkthrough of one subscription's lifecycle on Airwallex Billing, built in the sandbox with Python.

## Problem
Subscription businesses selling across currencies lose recurring revenue to failed renewals, not only to cancellations. Finance teams then struggle to see why a renewal failed, whether it recovered, and which payment settled which invoice. This repo follows one subscription through its billing lifecycle on Airwallex to see how much of that is visible and recoverable in one system.

## Who this is for
A mid-market subscription business in Asia selling in several currencies, with a finance team but no large engineering team. Outgrown a basic billing tool, but not at the scale where a heavy enterprise payments setup makes sense.

## Hypothesis
For this kind of business, one platform handling billing, payments and reconciliation should let a failed renewal be traced from invoice to payment attempt to retry to settlement through one ID chain, with no manual matching.

**Assumption to validate (not tested here):** that this buyer exists and feels this pain. That takes customer discovery, not a sandbox.

## Scope
**Built and tested:** customer, product, monthly price in a non-home currency, subscription via Billing Checkout, failed renewal, retry schedule, final UNPAID/CANCELLED state, webhooks, billing transactions (invoice to payment ID chain), one one-off invoice.

**Studied, not built:** usage-based billing, credit notes, tax, alternative payment methods.

## How I test it
1. Create a customer, product and monthly recurring price in a non-home currency.
2. Start a subscription through hosted Billing Checkout (AUTO_CHARGE).
3. Force a renewal to fail with a sandbox test card.
4. Record the retry schedule, final subscription status and webhook sequence.
5. Check whether the invoice links to a billing transaction, its Payment Intent and the payment attempt.
6. Create one one-off invoice.

## What this cannot show
The sandbox uses simulated money. It cannot prove approval-rate uplift or real recovery rates. It only shows what is visible and traceable in the product.

## Questions I'd ask a customer
(added after the build)

## What I'd tell a customer
(CFO version and CTO version, added after the build)

## Setup
1. Copy `.env.example` to `.env` and add your sandbox Client ID and API key.
2. `python3 -m pip install requests python-dotenv`
3. Run the scripts in order.

## Status
- [ ] 01 authenticate
- [ ] 02 customer, product, price
- [ ] 03 subscription via checkout
- [ ] 04 failed renewal and retries
- [ ] 05 webhooks and billing transactions
- [ ] 06 one-off invoice

Built by Ploypalin Tan. Sandbox only; not affiliated with Airwallex.
