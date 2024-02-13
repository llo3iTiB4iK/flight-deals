import os
import requests

sheety_url = os.environ.get("SHEETY_ENDPOINT")
bearer_headers = {"Authorization": f"Bearer {os.environ.get('BEARER_TOKEN')}"}


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        response = requests.get(url=f"{sheety_url}/prices", headers=bearer_headers)
        response.raise_for_status()
        self.destination_data = response.json()["prices"]
        response = requests.get(url=f"{sheety_url}/users", headers=bearer_headers)
        response.raise_for_status()
        self.customer_data = response.json()["users"]

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{sheety_url}/prices/{city['id']}", json=new_data, headers=bearer_headers)
            response.raise_for_status()
