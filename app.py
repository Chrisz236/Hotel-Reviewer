# Author:  Haolin Zhang
# Email:   zhanghaolin66@gmail.com
# File:    app.py
# Date:    Aug 14, 2023
# Version: 1.0

import os
import openai
from flask import Flask, request
from scraper import get_reviews_by_name_address_city

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/reviews', methods=['GET'])
def summary():
    """API end-point

        Returns
        -------
        summarized_reviews : str
            single paragraph of summary
    """
    hotel_name = request.args.get('hotel', '')
    address = request.args.get('address', '')
    city = request.args.get('city', '')
    debug = request.args.get('debug', 'false')

    reviews = get_reviews_by_name_address_city(hotel_name, address, city)

    # Print reviews in console if debug is enabled
    if debug.lower() == 'true':
        print('-' * 40 + " REVIEWS " + '-' * 40)
        print(reviews)
        print('-' * 89)
    
    return review_summary(reviews)


def review_summary(reviews):
    """Summarize reviews from TripAdvisor.com

        Parameters
        ----------
        reviews : str
            latest 5 reviews of hotel
        
        Returns
        -------
        summarized_reviews : str
            single paragraph of summary
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a highly skilled in summarizing content, you will provided with customers reviews about specific hotels. Your job is to summarize the content to one paragraph without complementing any additional information. If no reviews shows below, response No Data Available."
            },
            {
                "role": "user",
                "content": reviews
            }
        ]
    )

    return response['choices'][0]['message']['content']


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=4878,
        debug=True
    )