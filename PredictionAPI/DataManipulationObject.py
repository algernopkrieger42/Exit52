from datetime import datetime
import pandas as pd

class DataManipulationObject:
    def __init__(self):
        self.hour = datetime.now().hour
        self.denominator = 1

    def makeDF(self):
        df = pd.DataFrame([[0.0, 0.0, 0.0, 0.0]], columns=['avgTemp', 'maxTemp', 'minTemp', 'precip'], dtype=float)
        df.to_csv("Data/CurrentAverages/CurrentAverages.csv", index=False)

    def getHour(self):
        return self.hour

    def setHour(self):
        self.hour = datetime.now().hour

    def resetDenominator(self):
        self.denominator = 1

    def iterateDenominator(self):
        self.denominator += 1

    def getNewCurrent(self):
        return pd.read_csv("Data/CurrentData/CurrentWeather.csv")

    def getCurrentAverages(self):
        return pd.read_csv('Data/CurrentAverages/CurrentAverages.csv')

    def getForecastAverages(self):
        return pd.read_csv('Data/CurrentAverages/Todays_Manipulated_Forecast.csvt.csv')

    def averagingCurrentTemp(self, currentAvgTemp, newTemp):
        hour = self.getHour()
        newAvgTemp = (currentAvgTemp * (hour - 1) + newTemp) / hour
        return newAvgTemp

    def manipulateForecastData(self):
        df = pd.read_csv('Data/CurrentData/TodaysHourlyForecast.csv')
        df = df[['temp', 'precip']]
        df['low'] = df['temp']
        df['high'] = df['temp']

        for x in range(1, len(df.index)):
            df.loc[df.index[x - 1], 'temp'] = df.loc[x:len(df.index), 'temp'].mean()
            df.loc[df.index[x - 1], 'low'] = df.loc[x:len(df.index), 'low'].min()
            df.loc[df.index[x - 1], 'high'] = df.loc[x:len(df.index), 'high'].max()
            df.loc[df.index[x - 1], 'precip'] = df.loc[x:len(df.index), 'precip'].sum()
        df.to_csv('Data/CurrentAverages/Todays_Manipulated_Forecast.csv', index=False)


testObject = DataManipulationObject()
testObject.makeDF()
currentAverages = testObject.getCurrentAverages()
print(currentAverages.loc[0,'avgTemp'])