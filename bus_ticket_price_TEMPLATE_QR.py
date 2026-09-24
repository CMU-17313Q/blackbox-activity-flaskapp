"""
Compute the price of a bus ride:
  - Base fare is QAR 3
  - Children under 2 ride for free
  - People under 18 and senior citizens over 65 pay half the fare  
  - On weekdays (Monday to Friday), between 7 AM and 9 AM
    and between 4PM and 6PM a peak surcharge of QAR 1.5 is added.
  - Short trips under 5 minutes during off-peak time are free,
    except on weekends.
"""
def busTicketPrice(age: int, 
                   ride_datetime: datetime, 
                   ride_duration: int) -> float:
    ...
    

