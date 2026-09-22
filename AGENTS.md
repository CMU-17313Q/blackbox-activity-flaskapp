# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A single-route Flask app that implements a `bus_ticket_price(age, ride_datetime, ride_duration)`
function against a written specification, and renders a form for entering age/date/time/duration
and displaying the computed price. It supports an in-class activity for **17-313: Foundations of
Software Engineering** (CMU) on the "Software Specifications" lecture: students are given only the
spec (shown on the page itself, in the `specs` HTML string in `app.py`) and use specification-based
testing techniques (equivalence partitioning, boundary-value analysis, pairwise/combinatorial
testing) to design a test suite and find bugs in the implementation.

`bus_ticket_price_TEMPLATE.py` is the blank version of the exercise handed to students (spec in the
docstring, no implementation) - it mirrors the real function in `app.py` and is not imported by the
app.

## IMPORTANT: this repo intentionally ships a bug

**Do not "fix" `bus_ticket_price` in `app.py`, and do not reveal or hint at the bug in any
student-facing content (README, docstrings, on-page spec, error messages), unless the user
explicitly asks you to fix it.**

The known bug (marked with the `BUG:` comment at app.py:44): the peak-hour surcharge is computed
purely from time-of-day and applied unconditionally, even on weekends. A Saturday/Sunday ride that
falls in the 7-9am or 4-6pm window is incorrectly charged the weekend flat rate *plus* the $1.5
surcharge (e.g. $3.50 instead of the correct $2.00). It's a deliberate illustration of why
interaction/pairwise testing matters - a suite that tests "a weekend case" and "a peak-hours case"
separately, but never the combination, misses it.

## Running the app

No virtualenv is currently set up beyond the checked-in `venv/` (not to be relied on / recreated
without asking). To run locally:

```bash
pip install -r requirements.txt   # or: pipenv install (Pipfile targets Python 3.9)
FLASK_APP=app.py flask run
```

Or via Docker (matches `Dockerfile`, Python 3.9-slim, exposes port 5000):

```bash
docker build -t blackbox-activity-flaskapp .
docker run -p 5000:5000 blackbox-activity-flaskapp
```

There is no test suite, linter, or CI config in this repo.

## Deployment note

`vercel.json` points its build at `./api/app.py`, but no `api/` directory exists in this repo - the
actual Flask entry point is `app.py` at the repo root. Treat the Vercel config as stale/unverified
rather than authoritative if working on deployment.

## Architecture

Everything lives in `app.py`: it's a single Flask route (`/`, GET+POST) that builds the entire page
(styles, spec HTML, form, result) as concatenated HTML strings passed to
`render_template_string`, rather than using a `templates/` directory. On POST, form fields
(`age`, `trip-date`, `trip-time`, `duration`) are parsed into `bus_ticket_price`'s arguments and the
result is re-rendered into the same page.
