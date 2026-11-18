import os, json, uuid, requests
from dotenv import load_dotenv

load_dotenv(".env")
BASE = os.environ["AWX_BASE_URL"]
r = requests.post(f"{BASE}/api/v1/authentication/login", headers={
    "x-client-id": os.environ["AWX_CLIENT_ID"], "x-api-key": os.environ["AWX_API_KEY"]}, timeout=30)
H = {"Authorization": f"Bearer {r.json()['token']}", "Content-Type": "application/json"}
ids = json.load(open("ids.json"))

def post(path, body):
    r = requests.post(f"{BASE}{path}", headers=H, json={"request_id": str(uuid.uuid4()), **body}, timeout=30)
    print(path, "->", r.status_code)
    if not r.ok:
        print(r.text[:500]); raise SystemExit(1)
    return r.json()

p = post("/api/v1/billing/prices/create", {
    "product_id": ids["product_id"], "currency": "USD", "pricing_model": "FLAT",
    "flat_amount": 29, "billing_type": "IN_ADVANCE",
    "recurring": {"period": 1, "period_unit": "DAY"},
    "description": "Daily plan 29 USD (short cycle so dunning is observable)"})
ids["daily_price_id"] = p["id"]

c = post("/api/v1/billing/billing_checkouts/create", {
    "mode": "SUBSCRIPTION", "billing_customer_id": ids["customer_id"],
    "line_items": [{"price_id": p["id"], "quantity": 1}],
    "payment_options": {"payment_method_types": ["card"]},
    "subscription_data": {"duration": {"period": 30, "period_unit": "DAY"}},
    "success_url": "https://example.com/success", "back_url": "https://example.com/back",
    "ui_mode": "HOSTED"})
ids["checkout2_id"] = c["id"]
json.dump(ids, open("ids.json", "w"), indent=2)
print("open this URL and pay with 2223 0000 1018 1375:\n", c.get("url"))
