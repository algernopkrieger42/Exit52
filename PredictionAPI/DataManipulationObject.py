from datetime import datetime
import pandas as pd


class DataManipulator:
    def __init__(self):
        self.todaysPrediction = 100
        self.tomorrowsPrediction = 50

    def getTodaysPrediction(self):
        return self.todaysPrediction

    def getTomorrowsPrediction(self):
        return self.tomorrowsPrediction

    def updateTodaysPrediction(self, newTodaysPrediction):
        self.todaysPrediction = newTodaysPrediction

    def updateTomorrowsPrediction(self, newTomorrowsPrediction):
        self.tomorrowsPrediction = newTomorrowsPrediction

    def makeAveragesDF(self):
        df = pd.DataFrame([[0.0, 0.0, 0.0, 0.0]], columns=['avgTempF', 'maxTempF', 'minTempF', 'precipIn'], dtype=float)
        df.to_csv("Data/CurrentAverages/CurrentAverages.csv", index=False)

    def dfForModel(self):
        df = pd.DataFrame([[0.0, 0.0, 0.0, 0.0]], columns=['maxtempF', 'mintempF', 'avgtempF', 'totalprecipIn'],
                          dtype=float)
        return df

    def getHour(self):
        return datetime.now().hour

    def getNewCurrentWeather(self):
        return pd.read_csv("Data/CurrentData/CurrentWeather.csv")

    def getCurrentWeatherAverages(self):
        return pd.read_csv('Data/CurrentAverages/CurrentAverages.csv')

    def storeCurrentWeatherAverages(self, df):
        df.to_csv("Data/CurrentAverages/CurrentAverages.csv", index=False)

    def getForecastAverages(self):
        return pd.read_csv('Data/CurrentAverages/Todays_Manipulated_Forecast.csv')

    def manipulateForecastData(self):
        df = pd.read_csv('Data/CurrentData/TodaysHourlyForecast.csv')
        df = df[['temp', 'precip']]
        df.rename(columns={'temp': 'avgTempF', 'precip': 'precipIn'}, inplace=True)
        df['minTempF'] = df['avgTempF']
        df['maxTempF'] = df['avgTempF']

        for x in range(1, len(df.index)):
            df.loc[df.index[x - 1], 'avgTempF'] = df.loc[x:len(df.index), 'avgTempF'].sum()
            df.loc[df.index[x - 1], 'minTempF'] = df.loc[x:len(df.index), 'minTempF'].min()
            df.loc[df.index[x - 1], 'maxTempF'] = df.loc[x:len(df.index), 'maxTempF'].max()
            df.loc[df.index[x - 1], 'precipIn'] = df.loc[x:len(df.index), 'precipIn'].sum()
        df = df.drop(df.index[-1:])
        df.iloc[-1] = 0
        df.to_csv('Data/CurrentAverages/Todays_Manipulated_Forecast.csv', index=False)
