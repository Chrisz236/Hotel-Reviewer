# Author:  Haolin Zhang
# Email:   zhanghaolin66@gmail.com
# File:    scraper.py
# Date:    Aug 14, 2023
# Version: 1.0
# Description: Send request to TripAdvisor website and get first 10 reviews

import os
import requests
from urllib.parse import quote, unquote
from bs4 import BeautifulSoup
from rapidfuzz import fuzz

# developing only
TRIP_ARVISOR_API_KEY = os.getenv("TRIP_ADVISOR_API_KEY")

def get_location_id_by_name_address_city(name, address, city):
    """Get location_id of given hotel name

        Parameters
        ----------
        name : str
            Hotel name for query
        
        Returns
        -------
        location_id : str
            location_id of given hotel name
    """
    hotel_name = quote(name)
    address = quote(unquote(address).split(',', 1)[0])

    url = f"https://api.content.tripadvisor.com/api/v1/location/search?key={TRIP_ARVISOR_API_KEY}&searchQuery={hotel_name}&category=hotels&language=en"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    json_data = response.json()

    # This JSON contains up to 10 results from the query
    # Iterate list of JSON and fuzzy match the hotel that matches our address

    location_id = ""
    address_match_score = 0

    for i in range(len(json_data["data"])):
        # quick filter for city match
        if json_data["data"][i]["address_obj"]["city"].lower() == city.lower():

            similarity = fuzz.ratio(json_data["data"][i]["address_obj"]["address_string"].lower(), address.lower())
            if similarity > address_match_score:
                location_id = json_data["data"][i]["location_id"]
                address_match_score = similarity

    return location_id


def get_reviews_by_name_address_city(hotel_name, address):
    """Get reviews by given hotel name

        Parameters
        ----------
        hotel_name : str
            Hotel name for query
        
        Returns
        -------
        reviews : str
            latest reviews for given hotel name
    """
    location_id = get_location_id_by_name_address_city(hotel_name, address, city)
    url = f"https://www.tripadvisor.com/Hotel_Review-d{location_id}.html"
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')

    reviews = [
        rev.get_text("\n", strip=True)
        for rev in soup.select('div[data-test-target] > div[data-reviewid]')
    ][:5]

    return "\n\n".join(reviews)

if __name__ == '__main__':
    print(get_location_id_by_name_address_city("Bellagio Hotel &amp; Casino", "3600 Las Vegas Blvd S, Las VegasNevada 89109, Las Vegas, 89109, USA", "Las Vegas"))