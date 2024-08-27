from telnetlib import theNULL

import numpy as np
import pandas as pd

from DataManipulationObject import DataManipulationObject
from WeatherAPI import WeatherAPI
from datetime import datetime, time
import time
#from prediction_code import getPrediction



def main():
    try:
        timingTheStart()
    except Exception as e:
        print(f"an error occurred in the main function: {e}")


def timingTheStart():
    startTime = time(hour=23, minute=30, second=0)
    currentTime = datetime.now().time()
    while currentTime > startTime:
        time.sleep(300)
        currentTime = datetime.now().time()
    runningAPI()


def runningAPI():
    #instanciate weather api object
    weatherGetter = WeatherAPI()
    #instanciate object for data manipulation
    dataObject = DataManipulationObject()

    #time first hourly data call
    nextTime = time(hour=0, minute= 10, second = 0)
    currentTime = datetime.now().time()
    try:
        while True:
            if currentTime > nextTime:
                weatherGetter.getCurrent()
                #forecast data is only grabbed once a day
                if nextTime.hour is 0:
                    weatherGetter.getForecast()
                    time.sleep(5)
                    dataObject.manipulateForecastData()
                    dataObject.makeDF()
                updateAverages(dataObject)
                prepDataForModel(dataObject)
                nextHour = (currentTime.hour + 1) % 24
                nextTime = time(hour=nextHour, minute=0, second=0)
            else:
                time.sleep(300)
                currentTime = datetime.now().time()
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")
    except Exception as e:
        print(f"An error occurred in apiRunning: {e}")


def updateAverages(dataObject):
    newWeatherDF = dataObject.getNewCurrentWeather()
    currentAveragesDF = dataObject.getCurrentWeatherAverages()
    currentAveragesDF.loc[0,'avgTempF'] = currentAveragesDF.loc[0,'avgTempF'] + newWeatherDF.loc[0,'temp']
    currentAveragesDF.loc[0,'minTempF'] = min(currentAveragesDF.loc[0,'minTempF'], newWeatherDF.loc[0,'temp'])
    currentAveragesDF.loc[0,'maxTempF'] = max(currentAveragesDF.loc[0,'maxTempF'], newWeatherDF.loc[0,'temp'])
    currentAveragesDF.loc[0,'precipIn'] = currentAveragesDF.loc[0,'precipIn'] + newWeatherDF.loc[0,'precip']
    dataObject.storeCurrentWeatherAverages(currentAveragesDF)


def prepDataForModel(dataObject):
    modelData = dataObject.dfForModel()
    forecastData = dataObject.getForecastAverages()
    currentAverages = dataObject.getCurrentWeatherAverages()
    hour = dataObject.getHour()
    if hour != 23:
        modelData.loc[0,'avgTempF'] = (forecastData.loc[hour,'avgTempF'] + currentAverages.loc[0,'avgTemp']) / 24
        modelData.loc[0,'minTempF'] = min(forecastData.loc[hour,'minTempF'] + currentAverages.loc[0,'minTemp'])
        modelData.loc[0,'maxTempF'] = max(forecastData.loc[hour,'maxTempF'], currentAverages.loc[0,'maxTemp'])
        modelData.loc[0,'precipIn'] = forecastData.loc[hour,'precipIn'] + currentAverages.loc[0,'precipIn']
    else:
        modelData.loc[0, 'avgTempF'] = currentAverages.loc[0, 'avgTemp'] / 24
        modelData.loc[0, 'minTempF'] = currentAverages.loc[0, 'minTemp']
        modelData.loc[0, 'maxTempF'] = currentAverages.loc[0, 'maxTemp']
        modelData.loc[0, 'precipIn'] = currentAverages.loc[0, 'precipIn']

