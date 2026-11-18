import os, json, requests
from dotenv import load_dotenv

load_dotenv(".env")
BASE = os.environ["AWX_BASE_URL"]
r = requests.post(f"{BASE}/api/v1/authentication/login", headers={
    "x-client-id": os.environ["AWX_CLIENT_ID"], "x-api-key": os.environ["AWX_API_KEY"]}, timeout=30)
H = {"Authorization": f"Bearer {r.json()['token']}"}
ids = json.load(open("ids.json"))
s = requests.get(f"{BASE}/api/v1/billing/subscriptions/{ids['subscription_id']}", headers=H, timeout=30).json()
print("subscription status:", s.get("status"))
for k in ["latest_invoice_id", "collection_method", "next_billing_at", "next_payment_at"]:
    print(k, "->", s.get(k))
t = requests.get(f"{BASE}/api/v1/billing/billing_transactions/btxn_sgpv6lmp4ho9qtv9vo7", headers=H, timeout=30).json()
print("failed-invoice transaction status:", t.get("status"))
