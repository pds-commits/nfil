# Flexible Stripe checkout from Zoho CRM — design summary

Shared notes from the working session on replacing rigid Stripe **Payment Links** with per-deal **Checkout Sessions**, while keeping Zoho Flow able to resolve the Engagement.

**Demo mock in this folder:** open `README.md` to run the CRM-style UI locally.

---

## 1. Problem today

**Current AM path**

1. On an Engagement (Deal), select a fixed **Pay Plan (name)** combination.
2. Click **Create Payment Link**.
3. CRM looks up a pre-created row in **Stripe Payment Links** (catalog).
4. Appends `client_reference_id=<engagement_id>` on the Payment Link URL.
5. Saves the URL on the Engagement related list.
6. After payment, Zoho Flow receives Stripe webhooks and updates CRM / Books.

**Pain**

| Pain | Effect |
|---|---|
| Catalog rigidity | Can’t sell “12 flex hours” (or other non-SKU packs) without creating a new Stripe product/link (or doing it fully manually). |
| Discounts | Not supported from CRM. AM creates a Stripe coupon and sends a code for checkout. |
| Manual overflow | Custom qty/price → manual Stripe invoice + hand-entry into CRM/Books. |
| Goals | Close more / more flexible deals, with less ops friction. |

---

## 2. Recommended model (what to build)

**Stop** treating Stripe as a big catalog of ready-made Payment Links (one URL per plan combo).

**Start** treating CRM as the place where the **commercial offer** is configured, and create a **Checkout Session via API** when the AM clicks the button.

Keep a **small** Stripe product/price set (e.g. coaching hour, weekly, monthly rates) — not dozens of pre-built links.

```
CRM offer (plan, hours, rate, discount)
        ↓  button: Create Payment Link
Stripe Checkout Session (created at click time)
        ↓  customer pays
Stripe webhooks
        ↓
Zoho Flow → Engagement + Books (same idea as today)
```

### CRM offer fields (illustrative)

- Pay plan / billing mode (one-time block, weekly, monthly, …)
- Amount of hours (or units)
- Unit rate (default from plan; optional override with guardrails)
- Discount amount (or % — product decision)
- Read-only: subtotal, amount due
- Button keeps the familiar label **Create Payment Link** (engine changes underneath)

### What the button does

1. Validate offer fields.
2. Create Stripe **Checkout Session**:
   - `mode=payment` for one-time / flex blocks  
   - `mode=subscription` for weekly/monthly  
   - Line items from stable Price × quantity, or `price_data` if rate is custom  
   - Discount via Stripe Coupon (or equivalent) applied on the session  
   - **`client_reference_id` = Engagement / Deal id** (same contract as today)  
   - Also set **`metadata.engagement_id`** (and hours, plan, discount) as backup / richer fulfillment  
3. Save session URL (+ session id) on the Payment Links related list.
4. Prefer expiring/superseding older open sessions for that engagement (avoid double pay).

Subscriptions can be designed **in the same project** as one-time (not inherently “phase 2”). The extra work is CRM/Flow (renewals, dates, hours), not Stripe’s ability to create subscription checkouts.

---

## 3. Data flow (important: `client_reference_id` is not in the URL)

### Today (Payment Links)

Appending `?client_reference_id=<engagement_id>` on the Payment Link URL tells Stripe to stamp that value on the Checkout Session created when the customer opens the link.

Zoho Flow does **not** digests the URL. It digests the **webhook JSON**, which includes `client_reference_id`.

### Proposed (Checkout Sessions API)

Same end state, different write path:

1. CRM sets `client_reference_id` in the **Create Session API body**.
2. Customer opens `https://checkout.stripe.com/...` (URL has **no** engagement id).
3. Stripe fires webhooks; payload still includes `client_reference_id`.
4. Flow maps that → Engagement update (as today).

So the Flow contract stays: **webhook → `client_reference_id` → engagement id**.

---

## 4. Stripe webhook events

You already listen to **`checkout.session.completed`** and **`invoice.payment_succeeded`**. You do **not** need a wholesale event swap.

| Event | One-time Checkout (`mode=payment`) | Subscriptions (`mode=subscription`) |
|---|---|---|
| **`checkout.session.completed`** | **Primary.** Gate on `payment_status=paid` before fulfilling. Read `client_reference_id`, amounts, customer. | Fires when checkout finishes / sub starts. Good for initial engagement tie-back. |
| **`checkout.session.async_payment_succeeded`** / **`_failed`** | Add if you accept async methods (bank debits, etc.). | Same idea for async first payment. |
| **`invoice.payment_succeeded`** | Often **does not fire** unless you enable Checkout **invoice creation**. | **Keep.** First invoice + **renewals** (renewals usually have no new Checkout Session). |

**Practical**

- Keep both existing listeners.
- One-time flexible offers: fulfill mainly from **`checkout.session.completed`**.
- Recurring: keep **`invoice.payment_succeeded`** for renewals; use completed for initial `client_reference_id` tie-back.
- Deduplicate if both session + invoice fire for the same payment.
- Optional: enable `invoice_creation` on one-time sessions if much of Flow is invoice-shaped today.

---

## 5. Transition from current model → new model

Suggested path that limits blast radius:

### A. Parallel run (lowest risk)

1. Leave existing Payment Link catalog + button path working for standard SKUs.
2. Add offer fields + new button path (or enhance the same button with a feature flag / plan type).
3. New path creates Checkout Sessions with the same `client_reference_id` convention.
4. Confirm Flow still resolves engagement and updates CRM/Books for a few test deals (test mode first).
5. Cut sales over for flex / discounted / non-catalog offers first; then standard plans.

### B. Fulfillment must evolve with quantity

Today, post-payment logic often derives hours / pay plan from **fixed Books item names/units**. Variable quantities break that if you only change link creation.

Fulfillment should prefer:

- Offer fields saved on the Engagement when the link was created, and/or  
- Stripe **metadata** / line item quantity on the session/invoice  

…instead of assuming “this Books SKU always means N hours.”

### C. Catalog cleanup

- Keep a **small** Stripe product/price set.
- Stop creating new Payment Links for every qty combo.
- Existing Payment Links can remain for a while for old open deals; expire or stop using them for new sales.

### D. Cutover checklist

- [ ] Test mode: create session from CRM for flex + discount; pay; Flow updates correct Engagement  
- [ ] Confirm `client_reference_id` present on `checkout.session.completed`  
- [ ] Confirm Books customer/item/amount behavior for variable qty  
- [ ] Subscription path: first payment + one renewal  
- [ ] Double-pay: regenerate link expires previous open session  
- [ ] AM training: offer fields + when to use discount / rate override  
- [ ] Live cutover behind flag; monitor first week of deals  

---

## 6. Other things to consider

1. **Guardrails** — Floors/ceilings on rate and max discount %; manager approval outside policy. Flexibility without pricing chaos.
2. **Idempotency** — Don’t create duplicate sessions on double-click; store Stripe session id on the related-list row.
3. **Prefill** — `customer_email` / existing Stripe Customer id when known.
4. **Discounts** — Session-applied coupon (AM doesn’t share a code) vs promotion codes for marketing campaigns (keep both concepts separate).
5. **Books mapping** — Generic “coaching hours” item + amount from Stripe vs many SKUs; pick one strategy and align Flow.
6. **Subscriptions vs one-time in one release** — Doable; plan Flow renewals and engagement date/hours rules up front if sales needs both.
7. **Tax** — If you use Stripe Tax, configure registrations; don’t assume tax “just works.”
8. **Security** — Stripe secrets only in Zoho connections / server env — **never** in CRM fields, repos, or chat.
9. **UX naming** — Button can still say “Create Payment Link” even though the object is a Checkout Session URL.

---

## 7. What this mock shows

The HTML UI mimics an Engagement with offer fields and a related list. **Create Payment Link** creates a real Stripe **test-mode** Checkout Session with:

- `client_reference_id` = engagement id  
- metadata for plan / hours / discount  
- optional discount coupon on the session  

See `README.md` for how to run it. No secrets are stored in this repo; use a local test key if you want live session creation.

---

## 8. Decision summary

| Topic | Recommendation |
|---|---|
| Primary Stripe object for new sales links | **Checkout Session** (API at click), not pre-built Payment Links |
| Engagement correlation | **`client_reference_id` = Deal id** (+ metadata backup) |
| Flow webhooks | Keep **`checkout.session.completed`** + **`invoice.payment_succeeded`**; add async session events if needed |
| Discounts | Applied on session from CRM offer |
| Catalog | Small prices/products; quantity & discount on the offer |
| Migration | Parallel path → prove Flow → expand; update fulfillment for variable qty |
