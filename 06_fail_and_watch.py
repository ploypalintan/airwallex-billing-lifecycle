import os, json, time, uuid, datetime, requests
from dotenv import load_dotenv

load_dotenv(".env")
BASE = os.environ["AWX_BASE_URL"]
ids = json.load(open("ids.json"))
SUB = ids["subscription2_id"]

def hdr():
    r = requests.post(f"{BASE}/api/v1/authentication/login", headers={
        "x-client-id": os.environ["AWX_CLIENT_ID"], "x-api-key": os.environ["AWX_API_KEY"]}, timeout=30)
    return {"Authorization": f"Bearer {r.json()['token']}", "Content-Type": "application/json"}

def post(path, body):
    r = requests.post(f"{BASE}{path}", headers=hdr(), json={"request_id": str(uuid.uuid4()), **body}, timeout=30)
    print(path, "->", r.status_code)
    if not r.ok:
        print(r.text[:500]); raise SystemExit(1)
    return r.json()

def get(path):
    r = requests.get(f"{BASE}{path}", headers=hdr(), timeout=30)
    return r.json() if "json" in r.headers.get("content-type", "") else {}

p = post("/api/v1/billing/prices/create", {
    "product_id": ids["product_id"], "currency": "USD", "pricing_model": "FLAT",
    "flat_amount": 80.51, "billing_type": "IN_ADVANCE",
    "recurring": {"period": 1, "period_unit": "DAY"},
    "description": "Daily add-on 80.51 USD (forces decline)"})
post(f"/api/v1/billing/subscriptions/{SUB}/update", {
    "billing_action": "IMMEDIATE_CHARGE_AND_KEEP_CYCLE",
    "items": [{"price_id": p["id"], "quantity": 1, "proration_mode": "ALL"}]})
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
print("forced failure at", started, "- watching every 5 min (Ctrl+C to stop)")

def snapshot():
    s = get(f"/api/v1/billing/subscriptions/{SUB}")
    snap = {"subscription": s.get("status"), "invoices": []}
    for inv in get(f"/api/v1/billing/invoices?subscription_id={SUB}").get("items", []):
        row = {"id": inv["id"], "amount": inv.get("total_amount"),
               "status": inv.get("status"), "payment": inv.get("payment_status"), "tx": []}
        for t in get(f"/api/v1/billing/billing_transactions?invoice_id={inv['id']}").get("items", []):
            pi = get(f"/api/v1/pa/payment_intents/{t.get('external_id')}") if t.get("external_id") else {}
            a = pi.get("latest_payment_attempt") or {}
            row["tx"].append({"tx": t["id"], "tx_status": t.get("status"), "pi": t.get("external_id"),
                              "pi_status": pi.get("status"), "attempt": a.get("id"),
                              "attempt_status": a.get("status"), "failure": a.get("failure_code")})
        snap["invoices"].append(row)
    return snap

last = None
for _ in range(60):
    snap = snapshot()
    if snap != last:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        print("\n", now); print(json.dumps(snap, indent=1))
        open("evidence/retry_log.jsonl", "a").write(json.dumps({"at": now, **snap}) + "\n")
        last = snap
    time.sleep(300)
