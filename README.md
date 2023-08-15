# Hotel Reviewer
A Python Flask API endpoint to query the hotel with name and city, get its reviews and return as JSON string

## Setup
* Clone the repo `https://github.com/Chrisz236/Hotel-Reviewer.git`
* Setup your own OpenAI API key `export OPENAI_API_KEY={openai api key}`
* Setup your TripAdvisor API key `export TRIP_ADVISOR_API_KEY={tripadvisor api key}`
* Install required libs `pip3 install -r requirements.txt`
* Start service with `python3 app.py`

## Usage
`GET`: `http://{server-ip}:4878/reviews?hotel={hotel_name_in_url_format_encoded}`
e.g. `http://127.0.0.1:4878/reviews?hotel=Four%20Seasons%20Hotel%20San%20Francisco`