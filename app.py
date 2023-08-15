# Author:  Haolin Zhang
# Email:   zhanghaolin66@gmail.com
# File:    app.py
# Date:    Aug 14, 2023
# Version: 1.0

import os
import openai
from flask import Flask, request
from scraper import get_reviews_by_name

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
    reviews = get_reviews_by_name(hotel_name)
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
                "content": "You are a highly skilled AI trained in language comprehension and summarization about few hotel's review from different sources. I would like you to read the following reviews and summarize it into a concise single review about this place. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the pros and cons of this place and avoid using [some people say xxx, other people say xxx], but like you have been there on your own. Please avoid unnecessary details or tangential points."
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