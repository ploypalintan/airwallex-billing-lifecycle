import os, json, requests
from dotenv import load_dotenv

load_dotenv(".env")
BASE = os.environ["AWX_BASE_URL"]
r = requests.post(f"{BASE}/api/v1/authentication/login", headers={
    "x-client-id": os.environ["AWX_CLIENT_ID"], "x-api-key": os.environ["AWX_API_KEY"]}, timeout=30)
H = {"Authorization": f"Bearer {r.json()['token']}"}
ids = json.load(open("ids.json"))
c = requests.get(f"{BASE}/api/v1/billing/billing_checkouts/{ids['checkout_id']}", headers=H, timeout=30).json()
print("checkout status:", c.get("status"), "| subscription:", c.get("subscription_id"), "| payment source:", c.get("payment_source_id"))
if c.get("subscription_id"):
    ids["subscription_id"] = c["subscription_id"]
    json.dump(ids, open("ids.json", "w"), indent=2)
    s = requests.get(f"{BASE}/api/v1/billing/subscriptions/{c['subscription_id']}", headers=H, timeout=30).json()
    for k in ["status", "collection_method", "currency", "latest_invoice_id", "current_period_start", "current_period_end"]:
        print(k, "->", s.get(k))
