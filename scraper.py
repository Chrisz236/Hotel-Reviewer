# Author:  Haolin Zhang
# Email:   zhanghaolin66@gmail.com
# File:    scraper.py
# Date:    Aug 14, 2023
# Version: 1.0
# Description: Send request to TripAdvisor website and get first 10 reviews

import os
import openai
import requests
from urllib.parse import quote, unquote
from bs4 import BeautifulSoup

debug = True

TRIP_ARVISOR_API_KEY = os.getenv("TRIP_ADVISOR_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

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

    # print(json_data)

    # This JSON contains up to 10 results from the query
    # Iterate list of JSON and fuzzy match the hotel that matches our address

    address = unquote(address)

    # Smart semantic search for locations use GPT
    # Better performance than using classic fuzzy match
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a AI assistant trained and skilled in help people finding if two address are same. You will be provided 10 places with name, city, address and location_id, also a target place to found in this list. You task is to find the BEST match of given target place in list and return its location_id."
            },
            {
                "role": "user",
                "content": f"Your need to find: {name} at city: {city}, with address: {address} from the following list:\n{json_data}\n\nYou should ONLY return the location_id itself, without any other word."
            }
        ]
    )

    return response['choices'][0]['message']['content']


def get_reviews_by_name_address_city(hotel_name, address, city):
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

    result = "\n\n".join(reviews)

    if debug:
        print(f"[Reviews for {hotel_name} at {address}]")
        print(f"[Source: {url}]")

    return result