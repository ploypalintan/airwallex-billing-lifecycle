import os, json, requests
from dotenv import load_dotenv

load_dotenv(".env")
BASE = os.environ["AWX_BASE_URL"]
r = requests.post(f"{BASE}/api/v1/authentication/login", headers={
    "x-client-id": os.environ["AWX_CLIENT_ID"], "x-api-key": os.environ["AWX_API_KEY"]}, timeout=30)
H = {"Authorization": f"Bearer {r.json()['token']}"}
ids = json.load(open("ids.json"))

def get(path):
    r = requests.get(f"{BASE}{path}", headers=H, timeout=30)
    print(path.split("?")[0], "->", r.status_code)
    return r.json() if r.headers.get("content-type", "").startswith("application/json") else {}

invs = get(f"/api/v1/billing/invoices?subscription_id={ids['subscription_id']}")
for inv in invs.get("items", []):
    print("\nINVOICE", {k: inv.get(k) for k in ["id", "status", "total_amount", "amount_due", "payment_status", "created_at"]})
    tx = get(f"/api/v1/billing/billing_transactions?invoice_id={inv['id']}")
    for t in tx.get("items", []):
        print("  TRANSACTION", {k: t.get(k) for k in ["id", "type", "status", "amount", "external_id"]})
        if t.get("type") == "PAYMENT" and t.get("external_id"):
            pi = get(f"/api/v1/pa/payment_intents/{t['external_id']}")
            print("    PAYMENT INTENT", {k: pi.get(k) for k in ["id", "status", "amount", "currency"]})
            lpa = pi.get("latest_payment_attempt") or {}
            print("    LATEST ATTEMPT", {k: lpa.get(k) for k in ["id", "status", "failure_code", "authorization_code"]})
