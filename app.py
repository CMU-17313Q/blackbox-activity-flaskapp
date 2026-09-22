from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)


specs = """
<div class="function-specification">
    <h2>Bus Ticket Pricing Rules</h2>
    <ul>
        <li>The base fare is $3.</li>
        <li>Children under 2 ride for free.</li>
        <li>Children under 18 and senior citizens over 65 pay half the fare.</li>
        <li>On weekdays (Monday to Friday), between 7am and 9am and between 4pm and 6pm, a peak surcharge of $1.5 is added to the fare.</li>
        <li>During weekends (Saturday and Sunday), there is a flat rate of $2 for all riders, except for children under 2 who still ride for free.</li>
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
    is_weekend = weekday >= 5
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
        <title>Bus Ticket Price Calculator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                padding: 20px;
            }
            form {
                max-width: 600px;
                margin: auto;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 5px;
            }
            input, select {
                width: 100%;
                padding: 10px;
                font-size: 16px;
            }
            input[type="submit"] {
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
                font-size: 18px;
            }
            input[type="submit"]:hover {
                background-color: #45a049;
            }
            .price-display {
                font-size: 30px;
                margin-top: 20px;
            }
    .function-specification ul {
            list-style-type: none;
            padding: 0;
        }
        .function-specification li::before {
            content: "• ";
            color: #4CAF50; /* Bullet color */
        }
        .function-specification li {
            margin-bottom: 10px;
        }
        </style>
    </head>
    '''

    form_html = '''
    <form method="post">
    <div class="form-group">
        Age: <input type="number" name="age" min="0" max="117"required  value="{{ request.form['age']}}" /><br>
       </div>
            <div class="form-group">
        Date and Time (YYYY-MM-DD HH:MM): <input type="date" id="date" name="trip-date" min="2025-10-29" max="2029-12-31" value="{{ request.form['trip-date'] }}"/>
       </div>
            <div class="form-group">
    <input type="time" id="appt" name="trip-time" min="00:00" max="23:59" required value="{{ request.form['trip-time']}}" /><br>
       </div>
            <div class="form-group">
        Ride Duration (minutes): <input type="number" name="duration" min="0" max="120" required value="{{ request.form['duration']}}" /><br>
       </div>
            <div class="form-group">
        <input type="submit" value="Calculate Price">
    </form>
    <div class="price-display">Price: <span style="visibility: {{visibility}};">${{price}}</span></div>
    </body>
    </html>
    '''

    visibility = "hidden" if price == "" else "visible"
    return render_template_string(html_head+specs+form_html, price=price, visibility=visibility)
