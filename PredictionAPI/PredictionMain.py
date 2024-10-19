import json
import time
from datetime import datetime, timedelta
from datetime import time as a_time
from DataManipulationObject import DataManipulator
from PredictionSoftware import SnowPredictor
from WeatherAPI import WeatherGetter
import pandas as pd


def main():
    try:
        timingTheStart()
    except Exception as e:
        print(f"an error occurred in the main function: {e.__class__.__name__}: {e}")


def timingTheStart():
    startTime = a_time(hour=0, minute=5, second=0)
    currentTime = datetime.now().time()
    print("made it to timing the thing")
    while currentTime > startTime:
        time.sleep(180)
        currentTime = datetime.now().time()
    runningAPI()


def runningAPI():
    #instanciate weather api object
    weather = WeatherGetter()
    #instanciate object for data manipulation
    dataObject = DataManipulator()
    #time first hourly data call
    currentTime = datetime.now()
    nextTime = currentTime.replace(minute=0, second=0, microsecond=0)
    predictionObject = SnowPredictor()
    try:
        while True:
            if currentTime > nextTime:
                #to the minute weather
                weather.getCurrent()
                #forecast data is only grabbed once a day
                if currentTime.hour == 0:
                    #tomorrows prediction becomes todays prediction
                    todaysPrediction = dataObject.getTomorrowsPrediction()
                    dataObject.updateTodaysPrediction(todaysPrediction)
                    #get daily forecast
                    weather.getForecast()
                    #prep forecast for use
                    dataObject.manipulateForecastData()
                    #make new df for real weather data
                    dataObject.makeAveragesDF()
                    #store final prediction for the previous day
                    current_date = datetime.now()
                    formatted_date = current_date.strftime("%-m/%-d/%y")
                    add_entry_to_csv('Predictions24:25.csv', formatted_date, dataObject.getTomorrowsPrediction())
                elif currentTime.hour == 13:
                    current_date = datetime.now()
                    tomorrow_date = current_date + timedelta(days=1)
                    formatted_tomorrow = tomorrow_date.strftime("%-m/%-d/%y")
                    add_entry_to_csv('Predictions24:25.csv', formatted_tomorrow, dataObject.getTomorrowsPrediction())
                #update real weather df
                updateAverages(dataObject)
                #combine forecast and real data for model
                modelData = prepDataForModel(dataObject)
                print("DATA FOR MODEL: ")
                print(modelData)
                #make prediction
                prediction = predictionObject.makePrediction(modelData)
                #store updated prediction
                dataObject.updateTomorrowsPrediction(prediction)
                #write to json
                bringJsonInfoTogether(dataObject)
                #setup next cycle time
                nextTime = (nextTime + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
                print("next time: " + str(nextTime))
            else:
                time.sleep(300)
                currentTime = datetime.now()
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")
    except Exception as e:
        print(f"An error occurred in apiRunning: {e}")


def add_entry_to_csv(file_name, new_date, new_prediction):
    try:
        # Read the existing CSV into a DataFrame
        df = pd.read_csv(file_name)

        # Create a new DataFrame with the new entry
        new_row = pd.DataFrame({'date': [new_date], 'prediction': [new_prediction]})

        # Concatenate the new row with the existing DataFrame
        df = pd.concat([df, new_row], ignore_index=True)

        # Save the updated DataFrame back to the CSV file
        df.to_csv(file_name, index=False)
        print(f"Added new entry and saved to {file_name}")
    except FileNotFoundError:
        print(f"File '{file_name}' not found. Please provide a valid CSV file.")
    except Exception as e:
        print(f"An error occurred: {e}")


def updateAverages(dataObject):
    #get new data and current averages
    newWeatherDF = dataObject.getNewCurrentWeather()
    currentAveragesDF = dataObject.getCurrentWeatherAverages()
    #update numbers for temps and precip
    currentAveragesDF.loc[0, 'avgTempF'] = currentAveragesDF.loc[0, 'avgTempF'] + newWeatherDF.loc[0, 'temp']
    currentAveragesDF.loc[0, 'maxTempF'] = max(currentAveragesDF.loc[0, 'maxTempF'], newWeatherDF.loc[0, 'temp'])
    currentAveragesDF.loc[0, 'precipIn'] = currentAveragesDF.loc[0, 'precipIn'] + newWeatherDF.loc[0, 'precip']
    #first hour of the day averages being zero is a problem
    if currentAveragesDF.loc[0, 'minTempF'] == 0:
        currentAveragesDF.loc[0, 'minTempF'] = newWeatherDF.loc[0, 'temp']
    else:
        currentAveragesDF.loc[0, 'minTempF'] = min(currentAveragesDF.loc[0, 'minTempF'], newWeatherDF.loc[0, 'temp'])
    dataObject.storeCurrentWeatherAverages(currentAveragesDF)


def prepDataForModel(dataObject):
    #grab forecast and averages data, create modelDF that will be passed to model
    modelData = dataObject.dfForModel()
    forecastData = dataObject.getForecastAverages()
    currentAverages = dataObject.getCurrentWeatherAverages()
    #hour indicates which row to get forecast data from
    hour = dataObject.getHour()
    if hour != 23:
        modelData.loc[0, 'avgtempF'] = (forecastData.loc[hour, 'avgTempF'] + currentAverages.loc[0, 'avgTempF']) / 24
        modelData.loc[0, 'mintempF'] = min(forecastData.loc[hour, 'minTempF'], currentAverages.loc[0, 'minTempF'])
        modelData.loc[0, 'maxtempF'] = max(forecastData.loc[hour, 'maxTempF'], currentAverages.loc[0, 'maxTempF'])
        modelData.loc[0, 'totalprecipIn'] = forecastData.loc[hour, 'precipIn'] + currentAverages.loc[0, 'precipIn']
    else:
        modelData.loc[0, 'avgtempF'] = currentAverages.loc[0, 'avgTempF'] / 24
        modelData.loc[0, 'mintempF'] = currentAverages.loc[0, 'minTempF']
        modelData.loc[0, 'maxtempF'] = currentAverages.loc[0, 'maxTempF']
        modelData.loc[0, 'totalprecipIn'] = currentAverages.loc[0, 'precipIn']
    return modelData


def bringJsonInfoTogether(dataObject):
    todaysDate = get_date()
    tomorrowDate = get_tomorrow_date()
    todaysPrediction = dataObject.getTodaysPrediction()
    tomorrowsPrediction = dataObject.getTomorrowsPrediction()
    toJson(todaysPrediction, tomorrowsPrediction, todaysDate, tomorrowDate)
    print(todaysDate + str(todaysPrediction))
    print(tomorrowDate + str(tomorrowsPrediction))


def determineOriginalIndicator(day):
    if 11 <= day <= 13:
        return "th's"
    elif day % 10 == 1:
        return "st's"
    elif day % 10 == 2:
        return "nd's"
    elif day % 10 == 3:
        return "rd's"
    else:
        return "th's"


def get_date():
    try:
        current_date = datetime.now()
        formatted_date = current_date.strftime("%-m/%-d/%y")
        todayStatement = "Today - " + str(formatted_date) + "'s" + " Prediction:"
        return todayStatement
    except Exception as e:
        print(f"an error occurred in get_date: {e}")


def get_tomorrow_date():
    try:
        current_date = datetime.now()
        tomorrow_date = current_date + timedelta(days=1)
        formatted_tomorrow = tomorrow_date.strftime("%-m/%-d/%y")
        dateStatement = "Tomorrow - " + str(formatted_tomorrow) + "'s" + " Prediction:"
        return dateStatement
    except Exception as e:
        print(f"an error occurred in get_tomorrow_date: {e}")


def toJson(todayPrediction, tomorrowPrediction, todayDate, tomorrowDate):
    with open("../ExpressServer/predictions.json", mode="w") as file:
        data = {
            "Todays_Prediction": todayPrediction,
            "Tomorrows_Prediction": tomorrowPrediction,
            "Todays_Date": todayDate,
            "Tomorrows_Date": tomorrowDate
        }
        json.dump(data, file)


main()
