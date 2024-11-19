from datetime import datetime
import pandas as pd
import traceback


class DataManipulator:
    def __init__(self):
        self.todaysPrediction = "0"
        self.tomorrowsPrediction = "0"

    def getTodaysPrediction(self):
        try:
            return self.todaysPrediction
        except Exception as e:
            print(f"Error in getTodaysPrediction: {str(e)}")
            print(traceback.format_exc())

    def getTomorrowsPrediction(self):
        try:
            return self.tomorrowsPrediction
        except Exception as e:
            print(f"Error in getTomorrowsPrediction: {str(e)}")
            print(traceback.format_exc())

    def updateTodaysPrediction(self, newTodaysPrediction):
        try:
            self.todaysPrediction = newTodaysPrediction
        except Exception as e:
            print(f"Error in updateTodaysPrediction: {str(e)}")
            print(traceback.format_exc())

    def updateTomorrowsPrediction(self, newTomorrowsPrediction):
        try:
            self.tomorrowsPrediction = newTomorrowsPrediction
        except Exception as e:
            print(f"Error in updateTomorrowsPrediction: {str(e)}")
            print(traceback.format_exc())

    def makeAveragesDF(self):
        try:
            df = pd.DataFrame([[0.0, 0.0, 0.0, 0.0]], columns=['avgTempF', 'maxTempF', 'minTempF', 'precipIn'],
                              dtype=float)
            df.to_csv("Data/CurrentAverages/CurrentAverages.csv", index=False)
        except Exception as e:
            print(f"Error in makeAveragesDF: {str(e)}")
            print(traceback.format_exc())

    def dfForModel(self):
        try:
            df = pd.DataFrame([[0.0, 0.0, 0.0, 0.0]], columns=['maxtempF', 'mintempF', 'avgtempF', 'totalprecipIn'],
                              dtype=float)
            return df
        except Exception as e:
            print(f"Error in dfForModel: {str(e)}")
            print(traceback.format_exc())

    def getHour(self):
        try:
            return datetime.now().hour
        except Exception as e:
            print(f"Error in getHour: {str(e)}")
            print(traceback.format_exc())

    def getNewCurrentWeather(self):
        try:
            return pd.read_csv(
                'Data/CurrentData/Cleaned_CurrentWeather.csv',
                delimiter=",",
                quotechar='"',
                quoting=1,
                index_col=False  # Ensure no column is used as an index
            )
        except Exception as e:
            print(f"Error in getNewCurrentWeather: {str(e)}")
            print(traceback.format_exc())

    def getCurrentWeatherAverages(self):
        try:
            return pd.read_csv('Data/CurrentAverages/CurrentAverages.csv')
        except Exception as e:
            print(f"Error in getCurrentWeatherAverages: {str(e)}")
            print(traceback.format_exc())

    def storeCurrentWeatherAverages(self, df):
        try:
            df.to_csv("Data/CurrentAverages/CurrentAverages.csv", index=False)
        except Exception as e:
            print(f"Error in storeCurrentWeatherAverages: {str(e)}")
            print(traceback.format_exc())

    def getForecastAverages(self):
        try:
            return pd.read_csv('Data/CurrentAverages/Todays_Manipulated_Forecast.csv')
        except Exception as e:
            print(f"Error in getForecastAverages: {str(e)}")
            print(traceback.format_exc())

    def manipulateForecastData(self):
        try:
            df = pd.read_csv('Data/CurrentData/Cleaned_TodaysHourlyForecast.csv')
            df = df[['tempF', 'precipInches']]
            df.rename(columns={'tempF': 'avgTempF', 'precipInches': 'precipIn'}, inplace=True)
            df['minTempF'] = df['avgTempF']
            df['maxTempF'] = df['avgTempF']

            for x in range(1, len(df.index)):
                df.loc[df.index[x - 1], 'avgTempF'] = df.loc[x:len(df.index), 'avgTempF'].sum()
                df.loc[df.index[x - 1], 'minTempF'] = df.loc[x:len(df.index), 'minTempF'].min()
                df.loc[df.index[x - 1], 'maxTempF'] = df.loc[x:len(df.index), 'maxTempF'].max()
                df.loc[df.index[x - 1], 'precipIn'] = df.loc[x:len(df.index), 'precipIn'].sum()
            df = df.drop(df.index[-1:])
            #df.iloc[-1] = 0
            df.to_csv('Data/CurrentAverages/Todays_Manipulated_Forecast.csv', index=False)
        except Exception as e:
            print(f"Error in manipulateForecastData: {str(e)}")
            print(traceback.format_exc())
