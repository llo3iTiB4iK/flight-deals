import os
import requests

sheety_url = os.environ.get("SHEETY_ENDPOINT")
bearer_headers = {"Authorization": f"Bearer {os.environ.get('BEARER_TOKEN')}"}


def add_new_user(first_name, last_name, email):
    new_user = {
        "user": {
            "firstName": first_name,
            "lastName": last_name,
            "email": email
        }
    }
    response = requests.post(url=f"{sheety_url}/users", json=new_user, headers=bearer_headers)
    response.raise_for_status()
