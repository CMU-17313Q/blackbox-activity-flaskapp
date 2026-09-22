"""
Compute the price of a bus ride:
  - Base fare is $3
  - Children under 2 ride for free
  - People under 18 and senior citizens over 65 pay half the fare  
  - On weekdays (Monday to Friday), between 7am and 9am
    and between 4pm and 6pm a peak surcharge of $1.5 is added.
  - Short trips under 5min during off-peak time are free,
    except on weekends.
"""
def busTicketPrice(age: int, 
                   ride_datetime: datetime, 
                   ride_duration: int) -> float:
    ...
    