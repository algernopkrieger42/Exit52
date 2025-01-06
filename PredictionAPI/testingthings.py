from datetime import datetime

import pandas as pd
import pytz

'''from WeatherAPI import WeatherGetter
from DataManipulationObject import DataManipulator


dataObject = DataManipulator()



weatherObject = WeatherGetter()
weatherObject.getForecast()'''
'''
dataObject.manipulateForecastData()
weatherDF = dataObject.getForecastAverages()
print(weatherDF.info())
print(weatherDF.head(25))'''

pst = pytz.timezone("America/Los_Angeles")
currentTime = datetime.now(pst)

print("Aproaching the start. PST:",currentTime.time(),"MST:",datetime.now().time())

