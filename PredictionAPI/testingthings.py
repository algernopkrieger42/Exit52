import pandas as pd
from datetime import datetime



'''def manipulateForecastData():
    df = pd.read_csv('Data/CurrentData/TodaysHourlyForecast.csv')
    df = df[['temp', 'precip']]
    df['low'] = df['temp']
    df['high'] = df['temp']

    for x in range(1,len(df.index)):
        df.loc[df.index[x-1],'temp'] = df.loc[x:len(df.index),'temp'].mean()
        df.loc[df.index[x-1],'low'] = df.loc[x:len(df.index),'low'].min()
        df.loc[df.index[x - 1], 'high'] = df.loc[x:len(df.index), 'high'].max()
        df.loc[df.index[x-1], 'precip'] = df.loc[x:len(df.index), 'precip'].sum()
    df.to_csv('Data/CurrentAverages/Todays_Manipulated_Forecast.csv', index=False)'''

