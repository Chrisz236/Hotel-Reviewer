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

# developing only
TRIP_ARVISOR_API_KEY = os.getenv("TRIP_ADVISOR_API_KEY")

def get_location_id_by_name_and_address(name, address):
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

    url = f"https://api.content.tripadvisor.com/api/v1/location/search?key={TRIP_ARVISOR_API_KEY}&searchQuery={hotel_name}&category=hotels&address={address}&language=en"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    json_data = response.json()

    return str(json_data["data"][0]["location_id"])


def get_reviews_by_name_and_address(hotel_name, address):
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
    location_id = get_location_id_by_name_and_address(hotel_name, address)
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
