import urllib.request
from datetime import date
import traceback

class WeatherGetter:
    #Grab api testData once an hour
    def getCurrent(self):
        todaysDate = date.today().strftime('%Y-%m-%d')
        url2_current = "http://api.worldweatheronline.com/premium/v1/weather.ashx?key=e8cc942ed1bb45698e755158240411&q=47.4244,-121.4184&format=csv&fx=no&cc=yes&localObsTime=yes"

        try:
            # Download the CSV file
            file_path = "Data/CurrentData/CurrentWeather.csv"
            cleaned_file_path = "Data/CurrentData/Cleaned_CurrentWeather.csv"
            urllib.request.urlretrieve(url2_current, file_path)

            # Clean the downloaded CSV file
            with open(file_path, 'r') as original_file, open(cleaned_file_path, 'w') as cleaned_file:
                for i, line in enumerate(original_file, start=1):
                    # Skip lines 1-3 and line 5 (inclusive)
                    if i in range(1, 4) or i == 5:
                        continue

                    # Remove the leading '#' on the first column of line 4 (header)
                    if i == 4:
                        line = line.lstrip('#')  # Remove the leading '#' from the header

                    # Write the line to the cleaned file
                    cleaned_file.write(line)

        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code}")
        except urllib.error.URLError as e:
            print(f"URL Error: {e.reason}")
        except Exception as e:
            print(f"Error in getCurrent: {str(e)}")
            print(traceback.format_exc())



    def getForecast(self):
        todaysDate = date.today().strftime('%Y-%m-%d')
        url2_hourly = "http://api.worldweatheronline.com/premium/v1/weather.ashx?key=e8cc942ed1bb45698e755158240411&q=47.4244,-121.4184&format=csv&num_of_days=1&fx=yes&cc=no&tp=1"

        try:
            # Download the CSV file
            file_path = "Data/CurrentData/TodaysHourlyForecast.csv"
            cleaned_file_path = "Data/CurrentData/Cleaned_TodaysHourlyForecast.csv"
            urllib.request.urlretrieve(url2_hourly, file_path)

            # Clean the downloaded CSV file
            with open(file_path, 'r') as original_file, open(cleaned_file_path, 'w') as cleaned_file:
                for i, line in enumerate(original_file, start=1):
                    # Skip lines 1-5 and 7-9 (inclusive)
                    if i in range(1, 6) or i in range(7, 10):
                        continue

                    # Remove the leading '#' on the first column of row 6
                    if i == 6:
                        line = line.lstrip('#')  # Remove the leading '#' from the header

                    # Write the line to the cleaned file
                    cleaned_file.write(line)

        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code}")
        except urllib.error.URLError as e:
            print(f"URL Error: {e.reason}")
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
