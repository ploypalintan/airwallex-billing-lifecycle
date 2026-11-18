import os, json, uuid, requests
from dotenv import load_dotenv

load_dotenv(".env")
BASE = os.environ["AWX_BASE_URL"]
r = requests.post(f"{BASE}/api/v1/authentication/login", headers={
    "x-client-id": os.environ["AWX_CLIENT_ID"], "x-api-key": os.environ["AWX_API_KEY"]}, timeout=30)
H = {"Authorization": f"Bearer {r.json()['token']}", "Content-Type": "application/json"}
ids = json.load(open("ids.json"))
r = requests.post(f"{BASE}/api/v1/billing/subscriptions/{ids['subscription_id']}/update",
    headers=H, json={"request_id": str(uuid.uuid4()), "metadata": {"note": "webhook test"}}, timeout=30)
print(r.status_code, r.text[:200])
