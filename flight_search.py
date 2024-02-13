import os
import requests

FLIGHT_SEARCH_URL = "https://api.tequila.kiwi.com"
FLIGHT_SEARCH_API = os.environ.get("TEQUILA_API_KEY")
CURRENCY = "GBP"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.header = {"apikey": FLIGHT_SEARCH_API}

    def get_destination_code(self, city_name):
        location_endpoint = f"{FLIGHT_SEARCH_URL}/locations/query"
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_endpoint, headers=self.header, params=query)
        results = response.json()["locations"]
        code = results[0]["code"]
        return code

    def check_flights(self, FLY_FROM_IATA, FLY_TO_IATA, date_from, date_to, stop_overs=0):
        flight_parameters = {
            "fly_from": f"city:{FLY_FROM_IATA}",
            "fly_to": f"city:{FLY_TO_IATA}",
            "date_from": date_from.strftime("%d/%m/%Y"),
            "date_to": date_to.strftime("%d/%m/%Y"),
            "curr": CURRENCY,
            "max_stopovers": stop_overs,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1
        }
        response = requests.get(f"{FLIGHT_SEARCH_URL}/v2/search", params=flight_parameters, headers=self.header)
        response.raise_for_status()
        try:
            return response.json()['data'][0]
        except IndexError:
            if stop_overs == 0:
                return self.check_flights(FLY_FROM_IATA, FLY_TO_IATA, date_from, date_to, stop_overs=1)
            else:
                return None
