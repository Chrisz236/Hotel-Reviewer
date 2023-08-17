# Hotel Reviewer

> A smart search API

## Highlight

Enhanced Hotel Search with Large Language Models (LLMs)

## Background

In traditional search, if we want to compare if two string of name, or address is same, we usually do Fuzzy matching. We will compute the Levenshtein Distance (LD) of two strings and see if it looks same (literally)

However, this approach become less accurate when we want know if two name or address is same. For example: `Delano Las Vegas at Mandalay Bay` and string `Delano Las Vegas` has only `66.6%` similarity on LD but as human, we can tell it is same place

Similarly, two address are also considered same even if they are different on spell. As the human we know `123 ABC st. S` is same as `123 South ABC street` but LD shows us this two address has only `60.6%` similarity with is likely not make computer consider they are same.

Thus, we need to find out a way to actually understand two strings, like human, tells us if they are the same (semantically)

By using Large Language Models, we can easily determine two name, or address are the same with higher accuracy. It is perfect to deal with unformatted data source and perform the semantic match from dataset.

## Documentation
* **URL**

    `/reviews`

* **Method:**

    `GET`

* **URL Params**

    **Required:**

    `hotel=[string]`

    `address=[string]`

    `city=[string]`

    **Optional:**

    `debug=[string]`  (`true` or `false`) default `false`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{Summarized review of the hotel}`
 
* **Error Response:**

  * **Code:** 5xx <br />
    **Describe:** `Check your API key and try again`

* **Sample Call:**

  `curl /reviews?hotel={hotel_name}&address={address}&city={city}`

* **Notes:**

  The service will spawn on port `4878`

  Retry if you encounter `500` error code


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