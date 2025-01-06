import urllib.request
from datetime import date
import traceback
import requests
import pandas as pd

class WeatherGetter:
    def getCurrent(self):
        url = "http://api.worldweatheronline.com/premium/v1/weather.ashx"
        params = {
            "key": "e8cc942ed1bb45698e755158240411",
            "q": "47.4244,-121.4184",
            "format": "json",
            "fx": "no",
            "cc": "yes",
            "localObsTime": "yes"
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            current_condition = data.get("data", {}).get("current_condition", [{}])[0]
            temp_F = current_condition.get("temp_F")
            precipInches = current_condition.get("precipInches")
            df = pd.DataFrame(columns=['temp_F', 'precipInches'])
            df.loc[0] = [temp_F, precipInches]
            df.to_csv('Data/CurrentData/CurrentWeather.csv', index=False)

        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code}")
        except urllib.error.URLError as e:
            print(f"URL Error: {e.reason}")
        except KeyError as e:
            print(f"KeyError: Column missing in the data - {e}")
        except Exception as e:
            print(f"Error in getCurrent: {str(e)}")
            print(traceback.format_exc())


    def getForecast(self):
        url = "http://api.worldweatheronline.com/premium/v1/weather.ashx"
        params = {
            "key": "e8cc942ed1bb45698e755158240411",
            "q": "47.4244,-121.4184",
            "format": "json",
            "num_of_days": 1,
            "fx": "yes",
            "cc": "no",
            "tp": 1
        }

        # Make the API call
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()  # Convert response to JSON

            # Extract hourly data
            hourly_data = data["data"]["weather"][0]["hourly"]

            # Create a DataFrame with tempF and precipInches
            df = pd.DataFrame(hourly_data)
            df["tempF"] = df["tempF"].astype(float)
            df["precipInches"] = df["precipInches"].astype(float)
            df_filtered = df[["tempF", "precipInches"]]
            df_filtered.to_csv('Data/CurrentData/TodaysHourlyForecast.csv', index=False)
            print(df_filtered)

        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code}")
        except urllib.error.URLError as e:
            print(f"URL Error: {e.reason}")
        except KeyError as e:
            print(f"KeyError: Column missing in the data - {e}")
        except Exception as e:
            print(f"Error in getForecast: {str(e)}")
            print(traceback.format_exc())


# This function will create a CSV file `CleanedHourlyForecast.csv` that starts directly with the hourly data.


'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/47.4244,-121.4184/1990-11-01/1991-04-01/?unitGroup=us&include=hours&key=LVK3TNSG9UMRWNRTS7QABR2NQ&contentType=csv'
'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/47.4244,-121.4184/1990-11-01/1990-11-03/?unitGroup=us&include=days&key=LVK3TNSG9UMRWNRTS7QABR2NQ&contentType=csv'
'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/47.4219,-121.4217/1990-11-01/1991-04-30/?unitGroup=us&include=days&key=LVK3TNSG9UMRWNRTS7QABR2NQ&contentType=csv'

'''class WeatherGetter:
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

    def getTestingData(self):
        url1_current = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/47.4219,-121.4217/2023-11-01/2024-04-29/?unitGroup=us&include=days&key=LVK3TNSG9UMRWNRTS7QABR2NQ&contentType=csv'
        try:
            # Download the CSV file from the URL
            urllib.request.urlretrieve(url1_current, "Data/CurrentData/VisualCrossing23:24.csv")

        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code}")
        except urllib.error.URLError as e:
            print(f"URL Erroar: {e.reason}")


'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/47.4244,-121.4184/1990-11-01/1991-04-01/?unitGroup=us&include=hours&key=LVK3TNSG9UMRWNRTS7QABR2NQ&contentType=csv'
'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/47.4244,-121.4184/1990-11-01/1990-11-03/?unitGroup=us&include=days&key=LVK3TNSG9UMRWNRTS7QABR2NQ&contentType=csv'
'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/47.4219,-121.4217/1990-11-01/1991-04-30/?unitGroup=us&include=days&key=LVK3TNSG9UMRWNRTS7QABR2NQ&contentType=csv'
'''
