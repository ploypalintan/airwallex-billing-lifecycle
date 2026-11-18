import os, json, uuid, requests
from dotenv import load_dotenv

load_dotenv(".env")
BASE = os.environ["AWX_BASE_URL"]
r = requests.post(f"{BASE}/api/v1/authentication/login", headers={
    "x-client-id": os.environ["AWX_CLIENT_ID"], "x-api-key": os.environ["AWX_API_KEY"]}, timeout=30)
r.raise_for_status()
H = {"Authorization": f"Bearer {r.json()['token']}", "Content-Type": "application/json"}

ids = json.load(open("ids.json"))
body = {
    "mode": "SUBSCRIPTION",
    "request_id": str(uuid.uuid4()),
    "billing_customer_id": ids["customer_id"],
    "line_items": [{"price_id": ids["price_id"], "quantity": 1}],
    "payment_options": {
        "payment_method_types": ["card"],
    },
    "subscription_data": {"duration": {"period": 12, "period_unit": "MONTH"}},
    "success_url": "https://example.com/success",
    "back_url": "https://example.com/back",
    "ui_mode": "HOSTED",
}
r = requests.post(f"{BASE}/api/v1/billing/billing_checkouts/create", headers=H, json=body, timeout=30)
print(r.status_code)
if not r.ok:
    print(r.text[:500]); raise SystemExit(1)
d = r.json()
ids["checkout_id"] = d["id"]
json.dump(ids, open("ids.json", "w"), indent=2)
print("checkout id:", d["id"], "| status:", d["status"])
print("open this URL:", d.get("url"))
