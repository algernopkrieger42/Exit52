from datetime import time as a_time
from datetime import date, datetime, timedelta

current_date = datetime.now()
formatted_date = current_date.strftime("%-m/%-d/%y")
print(formatted_date)

tomorrow_date = current_date + timedelta(days=1)
formatted_tomorrow = tomorrow_date.strftime("%-m/%-d/%y")

print(formatted_tomorrow)

