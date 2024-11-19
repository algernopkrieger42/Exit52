from datetime import datetime

import pandas as pd

from WeatherAPI import WeatherGetter
from DataManipulationObject import DataManipulator


dataObject = DataManipulator()
'''newWeatherDF = dataObject.getNewCurrentWeather()
print(newWeatherDF.info())
print(newWeatherDF.head(25))
print(newWeatherDF.loc[0, 'temp_F'])
print(newWeatherDF.loc[0,'observation_time'])
print(newWeatherDF.loc[0,'temp_C'])'''
averagesDF = dataObject.getCurrentWeatherAverages()
print(averagesDF.info())
print(averagesDF.head())
#print(averagesDF.loc[])





