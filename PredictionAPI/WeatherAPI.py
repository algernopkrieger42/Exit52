

import urllib.request
from datetime import date


#Grab api testData once an hour
def weatherAPI():
    todaysDate = date.today()
    todaysDate = todaysDate.strftime('%Y-%m-%d')
    url1_current = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/snoqualmie%20pass?unitGroup=us&include=current&key=LVK3TNSG9UMRWNRTS7QABR2NQ&contentType=csv"
    url2_hourly = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/47.4244,-121.4184/" + todaysDate + "?unitGroup=us&include=hours&key=LVK3TNSG9UMRWNRTS7QABR2NQ&contentType=json"

    try:
        # Download the CSV file from the URL
        urllib.request.urlretrieve(url1_current, "RelevantData/Current_Hourly_Data/snoqualmie_pass_current.csv")
        urllib.request.urlretrieve(url2_hourly, "RelevantData/Current_Hourly_Data/snoqualmie_pass_hourly.csv")

    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code}")
    except urllib.error.URLError as e:
        print(f"URL Erroar: {e.reason}")


