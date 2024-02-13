from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

FLY_FROM_IATA = "LON"  # London IATA code

data_manager = DataManager()
notification_manager = NotificationManager()
flight_search = FlightSearch()

for city in data_manager.destination_data:
    if city["iataCode"] == "":
        code = flight_search.get_destination_code(city['city'])
        city["iataCode"] = code
data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_months_later = tomorrow + timedelta(days=180)

for city in data_manager.destination_data:
    cheapest_flight = flight_search.check_flights(FLY_FROM_IATA, city['iataCode'], tomorrow, six_months_later)

    if cheapest_flight and cheapest_flight['price'] < city['lowestPrice']:
        route = cheapest_flight['route']
        formatted_msg = f"Low price alert! Only £{cheapest_flight['price']} to fly from {cheapest_flight['cityFrom']}" \
                            f"-{cheapest_flight['flyFrom']} to {cheapest_flight['cityTo']}-{cheapest_flight['flyTo']}" \
                            f", from {route[0]['utc_departure'][:10]} to {route[-1]['utc_departure'][:10]}."
        if len(route) > 2:
            formatted_msg += f"\nFlight has 1 stop over, via {route[0]['cityTo']}"

        emails = [row["email"] for row in data_manager.customer_data]
        notification_manager.send_emails(emails, formatted_msg)
