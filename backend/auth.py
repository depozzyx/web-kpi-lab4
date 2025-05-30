import requests

CASDOOR_URL = "https://test-kpi-casdoor.pdf.yachts"

def verify_auth(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{CASDOOR_URL}/api/userinfo", headers=headers)

    if resp.status_code == 200:
        return resp.json() 
    else:
        return None