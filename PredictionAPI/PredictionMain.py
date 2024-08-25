import numpy as np
import pandas as pd

from DataManipulationObject import DataManipulationObject
from WeatherAPI import getCurrent, getForecast
#from prediction_code import getPrediction

def main():
    try:
        dataObject = DataManipulationObject()
        weatherGetter = WeatherAPI()
        theMeatOfThings(dataObject)
        #args for the main we can pass in if we want to obtain the testData at any given time

        #FUNCTION THAT WILL DO THE THINGS
    except Exception as e:
        print(f"an error occurred in the main function: {e}")

def theMeatOfThings(dataContainer):
    dataContainer.
