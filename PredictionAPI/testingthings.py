import time
from datetime import time as a_time
from datetime import date, datetime, timedelta
'''currentTime = datetime.now().time()
nextTime = a_time(hour=currentTime.hour, minute=0, second=0)

while True:
    if currentTime > nextTime:
        nextHour = (currentTime.hour + 1) % 24
        nextTime = a_time(hour=nextHour, minute=0, second=0)
        print("Current Time: " + str(currentTime))
        print("Next Time: " + str(nextTime))
    else:
        time.sleep(300)
        currentTime = datetime.now().time()'''

import time
from datetime import time as a_time
from datetime import datetime, timedelta

# Initialize current time
currentTime = datetime.now()
print(currentTime)
# Set the next target time (start from the next full hour)
nextTime = (currentTime + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
print(nextTime)
while True:
    # Check if the current time has passed or reached the nextTime
    if currentTime >= nextTime:
        # Update nextTime to the next full hour
        nextTime = (nextTime + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        # Print current time and next time
        print("Current Time: " + currentTime.strftime('%H:%M:%S'))
        print("Next Time: " + nextTime.strftime('%H:%M:%S'))



    else:
        # Sleep for 5 minutes before checking again
        time.sleep(300)
        currentTime = datetime.now()
