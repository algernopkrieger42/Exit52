import urllib.request
from datetime import date


class WeatherGetter:
#Grab api testData once an hour
    def getCurrent(self):
        url1_current = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/47.4244,-121.4184/?unitGroup=us&include=current&key=LVK3TNSG9UMRWNRTS7QABR2NQ&contentType=csv"
        try:
            # Download the CSV file from the URL
            urllib.request.urlretrieve(url1_current, "Data/CurrentData/CurrentWeather.csv")

        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code}")
        except urllib.error.URLError as e:
            print(f"URL Erroar: {e.reason}")


    def getForecast(self):
        todaysDate = date.today()
        todaysDate = todaysDate.strftime('%Y-%m-%d')
        url2_hourly = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/47.4244,-121.4184/" + todaysDate + "?unitGroup=us&include=hours&key=LVK3TNSG9UMRWNRTS7QABR2NQ&contentType=csv"
        try:
            urllib.request.urlretrieve(url2_hourly, "Data/CurrentData/TodaysHourlyForecast.csv")

        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code}")
        except urllib.error.URLError as e:
            print(f"URL Erroar: {e.reason}")
