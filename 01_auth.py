import os, requests
from dotenv import load_dotenv

load_dotenv(".env")
for base in ["https://api.sandbox.airwallex.com", "https://api-demo.airwallex.com"]:
    r = requests.post(
        f"{base}/api/v1/authentication/login",
        headers={
            "x-client-id": os.environ["AWX_CLIENT_ID"],
            "x-api-key": os.environ["AWX_API_KEY"],
        },
        timeout=30,
    )
    ok = r.ok and "token" in r.json()
    print(base, r.status_code, "token received" if ok else r.text[:100])
