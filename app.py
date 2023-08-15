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
                "content": "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points."
            },
            {
                "role": "user",
                "content": reviews
            }
        ]
    )
    return response['choices'][0]['message']['content']

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)