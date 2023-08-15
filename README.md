# Hotel Reviewer

## Documentation
* **URL**

    `/reviews`

* **Method:**

    `GET`

* **URL Params**

    **Required:**

    `hotel=[string]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{Summarized review of the hotel}`
 
* **Error Response:**

  * **Code:** 5xx <br />
    **Describe:** `Check your API key and try again`

* **Sample Call:**

  `curl /reviews?hotel=Hotel%20Name%20Goes%20Here`

* **Notes:**

  Retry if return `500` error code.


## Setup
Clone the repo 

```
git clone https://github.com/Chrisz236/Hotel-Reviewer.git
```

Setup your OpenAI API key 

```
export OPENAI_API_KEY={openai api key}
```

Setup your TripAdvisor API key 

```
export TRIP_ADVISOR_API_KEY={tripadvisor api key}
```

Install required libs 

```
pip3 install -r requirements.txt
```

Start service

```
python3 app.py
```