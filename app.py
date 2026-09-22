from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/blackboxapp'

specs = """
<div class="function-specification">
    <h2>Qatar Bus Ticket Pricing Rules</h2>
    <ul>
        <li>The base fare is QAR 3.</li>
        <li>Children under 2 ride for free.</li>
        <li>Children under 18 and senior citizens over 65 pay half the fare.</li>
        <li>On weekdays (Sunday to Thursday), between 7am and 9am and between 4pm and 6pm, a peak surcharge of QAR 1.5 is added to the fare.</li>
        <li>During weekends (Friday and Saturday), there is a flat rate of QAR 2 for all riders, except for children under 2 who still ride for free.</li>
        <li>Short trips under 5 minutes during off-peak times are free, except on weekends.</li>
    </ul>
</div>
"""

# Bus ticket price function (as previously defined)
def bus_ticket_price(age: int, ride_datetime: datetime,
                     ride_duration: int) -> float:

    from datetime import datetime, time

    price = 3.0
    weekday = ride_datetime.weekday()
    is_weekend = weekday in (4, 5)  # Qatar weekend: Friday, Saturday
    is_peak_time = (time(7, 0) <= ride_datetime.time() <= time(9, 0) or time(16, 0) <= ride_datetime.time() <= time(18, 0))
    is_short_trip = ride_duration < 5
    is_child_or_senior = age < 18 or age > 65
    is_infant = age < 2

    if is_infant:
        return 0.0
    if is_weekend:
        price = 2.0
    elif is_short_trip and not is_peak_time and not is_weekend:
        return 0.0
    elif is_child_or_senior:
        price /= 2

    """ BUG: peak times don't apply on weekends """
    if is_peak_time:
        price += 1.5

    return round(price, 2)
    # Function implementation here...

@app.route('/', methods=['GET', 'POST'])
def index():
    price = ""
    if request.method == 'POST':
        print(request)
        age = int(request.form['age'])
        tripdate = request.form['trip-date']
        triptime = request.form['trip-time']
        ride_datetime_str = f'{tripdate} {triptime}'
        print(ride_datetime_str)
        ride_datetime = datetime.strptime(ride_datetime_str, '%Y-%m-%d %H:%M')
        print(ride_datetime)
        ride_duration = int(request.form['duration'])
        price = bus_ticket_price(age, ride_datetime, ride_duration)
        print(price)

    # HTML form and result display
    html_head = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Qatar Bus Ticket Price Calculator</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Arial, sans-serif;
                background-color: #f5f5f7;
                padding: 30px 20px;
            }
            h2 {
                color: #8A1538;
            }
            form {
                max-width: 600px;
                margin: 0 auto 30px;
                background: #ffffff;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 6px;
                font-weight: 600;
                color: #333;
            }
            input {
                width: 100%;
                padding: 10px;
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 6px;
                box-sizing: border-box;
            }
            input[type="submit"] {
                background-color: #8A1538;
                color: white;
                border: none;
                cursor: pointer;
                font-size: 18px;
                padding: 12px 20px;
                border-radius: 6px;
                transition: background-color 0.2s ease-in-out;
            }
            input[type="submit"]:hover {
                background-color: #6b0f2b;
            }
            .price-display {
                max-width: 600px;
                margin: 0 auto;
                font-size: 32px;
                font-weight: bold;
                color: #8A1538;
                text-align: center;
            }
            .function-specification {
                max-width: 600px;
                margin: 0 auto 30px;
                background: #fdf2f5;
                border-left: 5px solid #8A1538;
                border-radius: 8px;
                padding: 25px 30px;
            }
            .function-specification h2 {
                font-size: 26px;
                margin-top: 0;
            }
            .function-specification ul {
                list-style-type: none;
                padding: 0;
                font-size: 18px;
                line-height: 1.7;
            }
            .function-specification li::before {
                content: "• ";
                color: #8A1538;
            }
            .function-specification li {
                margin-bottom: 12px;
            }
        </style>
    </head>
    '''

    form_html = '''
    <form method="post">
    <div class="form-group">
        <label for="age">Age</label>
        <input type="number" id="age" name="age" min="0" max="117" required value="{{ request.form['age']}}" />
       </div>
            <div class="form-group">
        <label for="date">Trip Date</label>
        <input type="date" id="date" name="trip-date" min="{{ min_date }}" max="2029-12-31" required value="{{ request.form['trip-date'] }}"/>
       </div>
            <div class="form-group">
        <label for="appt">Trip Time (24-hour, HH:MM)</label>
        <input type="time" id="appt" name="trip-time" min="00:00" max="23:59" required value="{{ request.form['trip-time']}}" />
       </div>
            <div class="form-group">
        <label for="duration">Ride Duration (minutes)</label>
        <input type="number" id="duration" name="duration" min="0" max="120" required value="{{ request.form['duration']}}" />
       </div>
            <div class="form-group">
        <input type="submit" value="Calculate Price">
    </form>
    <div class="price-display">Price: <span style="visibility: {{visibility}};">QAR {{price}}</span></div>
    </body>
    </html>
    '''

    visibility = "hidden" if price == "" else "visible"
    min_date = datetime.now().strftime('%Y-%m-%d')
    return render_template_string(html_head+specs+form_html, price=price, visibility=visibility, min_date=min_date)
