# Bus Ticket Pricing Activity

A small Flask app built for the "Software Specifications" lecture in
[17-313: Foundations of Software Engineering](https://cmu-17313q.github.io) at CMU.

The app implements a `bus_ticket_price(age, ride_datetime, ride_duration)` function against
the pricing rules below, and exposes a form where you can enter a rider's age, ride date, ride
time, and ride duration to see the computed price.

This app supports a specification-based testing exercise: given only the rules below (not the
implementation), design a test suite using techniques like equivalence partitioning,
boundary-value analysis, and pairwise/combinatorial testing, then explain the heuristics behind
your test cases. As a bonus, run your tests against the running app and see what you find.

## Setup

Requires Python 3.9.

Using pip:

```bash
pip install -r requirements.txt
```

Using pipenv:

```bash
pipenv install
```

## Running the app

```bash
FLASK_APP=app.py flask run
```

The app will be available at `http://127.0.0.1:5000`.

You can also run it with Docker:

```bash
docker build -t blackbox-activity-flaskapp .
docker run -p 5000:5000 blackbox-activity-flaskapp
```

## Using the app

Open the app in a browser and fill in the form: age, trip date, trip time, and ride duration
(in minutes). Submitting the form shows the computed ticket price.

The form submits a standard `POST /` request with these fields:

| Field | Description | Example |
|---|---|---|
| `age` | Rider's age in years | `30` |
| `trip-date` | Ride date, `YYYY-MM-DD` | `2025-11-03` |
| `trip-time` | Ride time, `HH:MM` (24-hour) | `08:15` |
| `duration` | Ride duration in minutes | `12` |

You can also submit this directly, for example with curl:

```bash
curl -X POST http://127.0.0.1:5000/ \
  -d "age=30" \
  -d "trip-date=2025-11-03" \
  -d "trip-time=08:15" \
  -d "duration=12"
```

The response is the same HTML page, with the price filled in.

## Pricing rules

- The base fare is $3.
- Children under 2 ride for free.
- Children under 18 and senior citizens over 65 pay half the fare.
- On weekdays (Monday to Friday), between 7am and 9am and between 4pm and 6pm, a peak
  surcharge of $1.5 is added to the fare.
- During weekends (Saturday and Sunday), there is a flat rate of $2 for all riders, except for
  children under 2 who still ride for free.
- Short trips under 5 minutes during off-peak times are free, except on weekends.
