import os, json, uuid, requests
from dotenv import load_dotenv

load_dotenv(".env")
BASE = os.environ["AWX_BASE_URL"]

def get_token():
    r = requests.post(f"{BASE}/api/v1/authentication/login", headers={
        "x-client-id": os.environ["AWX_CLIENT_ID"],
        "x-api-key": os.environ["AWX_API_KEY"]}, timeout=30)
    r.raise_for_status()
    return r.json()["token"]

TOKEN = get_token()
H = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def post(label, paths, body):
    body = {"request_id": str(uuid.uuid4()), **body}
    for p in paths:
        r = requests.post(f"{BASE}{p}", headers=H, json=body, timeout=30)
        print(f"{label}: {p} -> {r.status_code}")
        if r.status_code != 404:
            break
    if not r.ok:
        print(r.text[:400]); raise SystemExit(1)
    data = r.json()
    print(f"  id: {data.get('id')}")
    return data

customer = post("customer",
    ["/api/v1/billing/billing_customers/create", "/api/v1/billing_customers/create"],
    {"name": "Demo SaaS Pte Ltd", "email": "billing-demo@example.com",
     "type": "BUSINESS", "address": {"country_code": "SG"}})

product = post("product",
    ["/api/v1/billing/products/create", "/api/v1/products/create"],
    {"name": "Demo SaaS Plan"})

price = post("price",
    ["/api/v1/billing/prices/create", "/api/v1/prices/create"],
    {"product_id": product["id"], "currency": "USD", "pricing_model": "FLAT",
     "flat_amount": 29, "billing_type": "IN_ADVANCE",
     "recurring": {"period": 1, "period_unit": "MONTH"},
     "description": "Monthly plan, billed in USD"})

json.dump({"customer_id": customer["id"], "product_id": product["id"],
           "price_id": price["id"]}, open("ids.json", "w"), indent=2)
print("saved ids.json")
