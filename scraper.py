# Author:  Haolin Zhang
# Email:   zhanghaolin66@gmail.com
# File:    scraper.py
# Date:    Aug 14, 2023
# Version: 1.0
# Description: Send request to TripAdvisor website and get first 10 reviews

import requests
from urllib.parse import quote
from bs4 import BeautifulSoup

# developing only
TRIP_ARVISOR_API_KEY = "576E1C52C5144AB7A7D74D62E09E7A36"

def get_location_id_by_name(name):
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
    url = f"https://api.content.tripadvisor.com/api/v1/location/search?key={TRIP_ARVISOR_API_KEY}&searchQuery={hotel_name}&category=hotels&language=en"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    json_data = response.json()

    return str(json_data["data"][0]["location_id"])


def get_reviews_by_name(hotel_name):
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
    location_id = get_location_id_by_name(hotel_name)
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
    get_reviews_by_name("Homewood Suites by Hilton Newark-Fremont")