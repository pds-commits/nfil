#!/usr/bin/env python3
"""CRM mock server that creates Stripe Checkout Sessions from offer fields.

Colleague-friendly mode (recommended):
  put STRIPE_SECRET_KEY in a local .env (never commit it), then:
  python3 server.py

Then open http://127.0.0.1:8777/

Without a local Stripe key, Create Payment Link queues a job for an agent
bridge (dev only). Prefer the local env-key path for sharing.
"""

from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
PENDING = ROOT / "queue" / "pending"
DONE = ROOT / "queue" / "done"
FAILED = ROOT / "queue" / "failed"
PORT = int(os.environ.get("PORT", "8777"))
STRIPE_SECRET_KEY = (os.environ.get("STRIPE_SECRET_KEY") or "").strip()
STRIPE_API_BASE = "https://api.stripe.com/v1"

for d in (PENDING, DONE, FAILED):
    d.mkdir(parents=True, exist_ok=True)


def _json_response(handler: SimpleHTTPRequestHandler, status: int, payload: dict) -> None:
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    handler.wfile.write(body)


def _stripe_form(data: dict, prefix: str = "") -> list[tuple[str, str]]:
    """Flatten nested dicts/lists into Stripe form-encoded pairs."""
    pairs: list[tuple[str, str]] = []
    for key, value in data.items():
        full_key = f"{prefix}[{key}]" if prefix else key
        if value is None:
            continue
        if isinstance(value, dict):
            pairs.extend(_stripe_form(value, full_key))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                item_key = f"{full_key}[{i}]"
                if isinstance(item, dict):
                    pairs.extend(_stripe_form(item, item_key))
                else:
                    pairs.append((item_key, str(item)))
        elif isinstance(value, bool):
            pairs.append((full_key, "true" if value else "false"))
        else:
            pairs.append((full_key, str(value)))
    return pairs


def stripe_request(method: str, path: str, data: dict | None = None) -> dict:
    if not STRIPE_SECRET_KEY:
        raise RuntimeError("STRIPE_SECRET_KEY is not set")
    url = STRIPE_API_BASE + path
    body = None
    headers = {
        "Authorization": f"Bearer {STRIPE_SECRET_KEY}",
        "Stripe-Version": "2025-04-30.basil",
    }
    if data is not None:
        body = urllib.parse.urlencode(_stripe_form(data)).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        try:
            err_json = json.loads(err_body)
            message = err_json.get("error", {}).get("message") or err_body
        except json.JSONDecodeError:
            message = err_body or str(e)
        raise RuntimeError(f"Stripe API {e.code}: {message}") from e


def create_checkout_session(job: dict) -> dict:
    coupon_id = None
    if job["discount_cents"] > 0:
        coupon = stripe_request(
            "POST",
            "/coupons",
            {
                "name": f"CRM Offer Discount ${job['discount_cents'] / 100:.0f}",
                "amount_off": job["discount_cents"],
                "currency": "usd",
                "duration": "once",
                "max_redemptions": 1,
                "metadata": {
                    "engagement_id": job["engagement_id"],
                    "source": "crm_checkout_mock",
                    "job_id": job["job_id"],
                },
            },
        )
        coupon_id = coupon["id"]

    line_item = {
        "quantity": job["quantity"],
        "price_data": {
            "currency": "usd",
            "unit_amount": job["line_unit_amount_cents"],
            "product_data": {
                "name": job["product_name"],
                "description": (
                    f"{job['hours']:g} hours @ ${job['unit_rate']:g}/hr"
                    if job["hours_is_int"]
                    else f"Block totaling ${job['subtotal_cents'] / 100:.2f}"
                ),
            },
        },
    }

    session_payload: dict = {
        "mode": "payment",
        "success_url": "https://example.com/success?session_id={CHECKOUT_SESSION_ID}",
        "cancel_url": "https://example.com/cancel",
        "client_reference_id": job["client_reference_id"],
        "line_items": [line_item],
        "metadata": {
            "engagement_id": job["engagement_id"],
            "pay_plan": job["pay_plan"],
            "amount_of_hours": str(job["hours"]),
            "unit_rate_cents": str(job["unit_amount_cents"]),
            "discount_amount_cents": str(job["discount_cents"]),
            "source": "crm_checkout_mock",
            "job_id": job["job_id"],
        },
    }
    if job.get("customer_email"):
        session_payload["customer_email"] = job["customer_email"]
    if coupon_id:
        session_payload["discounts"] = [{"coupon": coupon_id}]

    session = stripe_request("POST", "/checkout/sessions", session_payload)
    return {
        "job_id": job["job_id"],
        "session_id": session["id"],
        "url": session["url"],
        "client_reference_id": job["client_reference_id"],
        "amount_total": session.get("amount_total"),
    }


def build_job(data: dict) -> dict:
    engagement_id = str(data.get("engagement_id") or "").strip()
    if not engagement_id:
        raise ValueError("engagement_id required")

    try:
        hours = float(data.get("hours") or 0)
        unit_rate = float(data.get("unit_rate") or 0)
        discount = float(data.get("discount") or 0)
    except (TypeError, ValueError) as e:
        raise ValueError("invalid numeric fields") from e

    if hours <= 0 or unit_rate <= 0:
        raise ValueError("hours and unit_rate must be > 0")

    subtotal_cents = int(round(hours * unit_rate * 100))
    discount_cents = int(round(max(0, discount) * 100))
    if discount_cents > subtotal_cents:
        discount_cents = subtotal_cents
    total_cents = subtotal_cents - discount_cents
    if total_cents <= 0:
        raise ValueError("amount due must be > 0")

    hours_is_int = abs(hours - round(hours)) < 1e-9
    job_id = uuid.uuid4().hex[:12]
    return {
        "job_id": job_id,
        "created_at": time.time(),
        "engagement_id": engagement_id,
        "client_reference_id": engagement_id,
        "pay_plan": str(data.get("pay_plan") or "Per Hour"),
        "hours": hours,
        "unit_rate": unit_rate,
        "discount": discount_cents / 100,
        "unit_amount_cents": int(round(unit_rate * 100)),
        "subtotal_cents": subtotal_cents,
        "discount_cents": discount_cents,
        "total_cents": total_cents,
        "hours_is_int": hours_is_int,
        "quantity": int(round(hours)) if hours_is_int else 1,
        "line_unit_amount_cents": int(round(unit_rate * 100))
        if hours_is_int
        else subtotal_cents,
        "customer_email": str(data.get("customer_email") or "").strip(),
        "product_name": str(
            data.get("product_name") or "Executive Function Coaching — Flex Hours"
        ),
    }


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt: str, *args) -> None:
        print(f"[crm-mock] {self.address_string()} - {fmt % args}")

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path != "/api/create-checkout":
            _json_response(self, 404, {"error": "not found"})
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            _json_response(self, 400, {"error": "invalid JSON"})
            return

        try:
            job = build_job(data)
        except ValueError as e:
            _json_response(self, 400, {"error": str(e)})
            return

        # Direct Stripe path (works without Cursor)
        if STRIPE_SECRET_KEY:
            try:
                result = create_checkout_session(job)
                done_path = DONE / f"{job['job_id']}.json"
                done_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
                print(
                    f"CHECKOUT_CREATED job_id={job['job_id']} "
                    f"session_id={result['session_id']} "
                    f"client_reference_id={job['client_reference_id']}",
                    flush=True,
                )
                _json_response(self, 202, {"job_id": job["job_id"], "status": "pending"})
            except Exception as e:  # noqa: BLE001 - surface to UI
                failed = {"job_id": job["job_id"], "error": str(e)}
                (FAILED / f"{job['job_id']}.json").write_text(
                    json.dumps(failed, indent=2), encoding="utf-8"
                )
                print(f"CHECKOUT_FAILED job_id={job['job_id']} error={e}", flush=True)
                _json_response(self, 202, {"job_id": job["job_id"], "status": "pending"})
            return

        # Agent-bridge fallback (Cursor MCP fulfills queue/pending)
        pending_path = PENDING / f"{job['job_id']}.json"
        pending_path.write_text(json.dumps(job, indent=2), encoding="utf-8")
        print(
            f"CHECKOUT_REQUEST job_id={job['job_id']} engagement_id={job['engagement_id']}",
            flush=True,
        )
        _json_response(self, 202, {"job_id": job["job_id"], "status": "pending"})

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/health":
            _json_response(
                self,
                200,
                {
                    "ok": True,
                    "stripe_key_configured": bool(STRIPE_SECRET_KEY),
                    "mode": "direct" if STRIPE_SECRET_KEY else "agent_bridge",
                },
            )
            return

        m = re.match(r"^/api/status/([a-f0-9]+)$", path)
        if not m:
            return super().do_GET()

        job_id = m.group(1)
        done_path = DONE / f"{job_id}.json"
        failed_path = FAILED / f"{job_id}.json"
        pending_path = PENDING / f"{job_id}.json"

        if done_path.exists():
            data = json.loads(done_path.read_text(encoding="utf-8"))
            _json_response(self, 200, {"status": "done", **data})
            return
        if failed_path.exists():
            data = json.loads(failed_path.read_text(encoding="utf-8"))
            _json_response(self, 200, {"status": "failed", **data})
            return
        if pending_path.exists():
            _json_response(self, 200, {"status": "pending", "job_id": job_id})
            return
        _json_response(self, 404, {"status": "unknown", "job_id": job_id})


def main() -> None:
    mode = "direct Stripe" if STRIPE_SECRET_KEY else "agent bridge (set STRIPE_SECRET_KEY)"
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"CRM checkout mock at http://127.0.0.1:{PORT}/", flush=True)
    print(f"Mode: {mode}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
