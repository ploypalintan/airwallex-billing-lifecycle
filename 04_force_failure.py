import os, json, uuid, requests
from dotenv import load_dotenv

load_dotenv(".env")
BASE = os.environ["AWX_BASE_URL"]
r = requests.post(f"{BASE}/api/v1/authentication/login", headers={
    "x-client-id": os.environ["AWX_CLIENT_ID"], "x-api-key": os.environ["AWX_API_KEY"]}, timeout=30)
H = {"Authorization": f"Bearer {r.json()['token']}", "Content-Type": "application/json"}
ids = json.load(open("ids.json"))

def post(path, body):
    body = {"request_id": str(uuid.uuid4()), **body}
    r = requests.post(f"{BASE}{path}", headers=H, json=body, timeout=30)
    print(path, "->", r.status_code)
    if not r.ok:
        print(r.text[:500]); raise SystemExit(1)
    return r.json()

def get(path):
    r = requests.get(f"{BASE}{path}", headers=H, timeout=30)
    print(path, "->", r.status_code)
    return r.json()

p2 = post("/api/v1/billing/prices/create", {
    "product_id": ids["product_id"], "currency": "USD", "pricing_model": "FLAT",
    "flat_amount": 80.51, "billing_type": "IN_ADVANCE",
    "recurring": {"period": 1, "period_unit": "MONTH"},
    "description": "Upgrade add-on, 80.51 USD (forces decline on test card)"})
ids["price2_id"] = p2["id"]; print("price2:", p2["id"])

sub = post(f"/api/v1/billing/subscriptions/{ids['subscription_id']}/update", {
    "billing_action": "IMMEDIATE_CHARGE_AND_KEEP_CYCLE",
    "items": [{"price_id": p2["id"], "quantity": 1, "proration_mode": "ALL"}]})
json.dump(ids, open("ids.json", "w"), indent=2)

s = get(f"/api/v1/billing/subscriptions/{ids['subscription_id']}")
print("subscription status:", s.get("status"), "| latest invoice:", s.get("latest_invoice_id"))
items = get(f"/api/v1/billing/subscriptions/{ids['subscription_id']}/items")
for it in items.get("items", []):
    print("  item:", it.get("id"), it.get("price_id"), "qty", it.get("quantity"))

inv_id = s.get("latest_invoice_id")
inv = get(f"/api/v1/billing/invoices/{inv_id}")
print("invoice:", {k: inv.get(k) for k in ["id", "status", "currency", "total_amount", "amount_due", "payment_status"]})
tx = get(f"/api/v1/billing/billing_transactions?invoice_id={inv_id}")
for t in tx.get("items", []):
    print("  transaction:", {k: t.get(k) for k in ["id", "type", "status", "amount", "currency", "external_id"]})
