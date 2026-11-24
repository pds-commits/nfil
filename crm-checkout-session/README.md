# CRM Checkout Session mock (NFIL)

Small Zoho CRM–style mock that shows how Account Managers could configure a flexible payment offer on an Engagement and create a **Stripe Checkout Session** on click — instead of picking a pre-built Payment Link from a catalog.

## What it demonstrates

- Offer fields on the Deal: pay plan, hours, unit rate, discount
- **Create Payment Link** builds a Checkout Session via Stripe API
- `client_reference_id` = Engagement / Deal id (same hook as today’s live Flow)
- Session URL saved into a Payment Links–style related list

This keeps the existing payment-processing contract (`client_reference_id` → engagement) while removing the rigid “one Stripe Payment Link per SKU combo” catalog.

## Run locally (no Cursor required)

Needs **Python 3** (stdlib only) and a Stripe **test-mode** secret from your own Dashboard (never commit it).

```bash
cd checkout-crm-mock
cp .env.example .env
# edit .env and paste your test secret locally
set -a && source .env && set +a
python3 server.py
```

Or export `STRIPE_SECRET_KEY` in your shell from your own Dashboard — do not paste keys into chat, PRs, or the repo.

Open [http://127.0.0.1:8777/](http://127.0.0.1:8777/)

1. Adjust hours / rate / discount if you want  
2. Click **Create Payment Link**  
3. Open the checkout URL  
4. Pay with Stripe’s published test card (see Stripe test cards docs)

Optional: `PORT=8780 python3 server.py`

Check mode: [http://127.0.0.1:8777/api/health](http://127.0.0.1:8777/api/health) should show `"mode": "direct"` when a key is loaded locally.

## Important

- **No secrets in this repo.** Keys stay in your local env / `.env` (gitignored).
- Use Stripe **test mode** only for this demo.
- Success/cancel URLs are placeholders (`example.com`); fine for this demo.

## Context

Today in CRM, AMs select a fixed **Pay Plan (name)** and the button looks up a pre-created Stripe Payment Link, then appends `client_reference_id`. Discounts and non-catalog quantities (e.g. 12 flex hours) require manual Stripe work.

This mock explores generating the checkout **at click time** from the offer fields, while still passing the engagement id as `client_reference_id` so downstream Zoho Flow → CRM/Books can stay mostly intact.
