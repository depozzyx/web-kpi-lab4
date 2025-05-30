import requests

from lib import config


def verify_auth(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{config.CASDOOR_URL}/api/userinfo", headers=headers)

    if resp.status_code == 200:
        return resp.json() 
    else:
        return None