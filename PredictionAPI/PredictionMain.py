import json
import time
from datetime import datetime, date, timedelta
from datetime import time as a_time
from DataManipulationObject import DataManipulator
from PredictionSoftware import getPrediction
from WeatherAPI import WeatherGetter



def main():
    try:
        timingTheStart()
    except Exception as e:
        print(f"an error occurred in the main function: {e.__class__.__name__}: {e}")


def timingTheStart():
    startTime = a_time(hour=0, minute=1, second=0)
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
    nextTime = a_time(hour=0, minute= 5, second = 0)
    currentTime = datetime.now().time()
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
                    print("made it to runningAPI at" + str(currentTime))
                #update real weather df
                updateAverages(dataObject)
                #combine forecast and real data for model
                modelData = prepDataForModel(dataObject)
                print(modelData)
                #make prediction
                prediction = getPrediction(modelData)
                #store updated prediction
                dataObject.updateTomorrowsPrediction(prediction)
                #write to json
                bringJsonInfoTogether(dataObject)
                #setup next cycle time
                nextHour = (currentTime.hour + 1) % 24
                nextTime = a_time(hour=nextHour, minute=0, second=0)
                print("next time: " + str(nextTime))
            else:
                time.sleep(300)
                currentTime = datetime.now().time()
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")
    except Exception as e:
        print(f"An error occurred in apiRunning: {e}")



def updateAverages(dataObject):
    #get new data and current averages
    newWeatherDF = dataObject.getNewCurrentWeather()
    currentAveragesDF = dataObject.getCurrentWeatherAverages()
    #update numbers for temps and precip
    currentAveragesDF.loc[0,'avgTempF'] = currentAveragesDF.loc[0,'avgTempF'] + newWeatherDF.loc[0,'temp']
    currentAveragesDF.loc[0,'maxTempF'] = max(currentAveragesDF.loc[0,'maxTempF'], newWeatherDF.loc[0,'temp'])
    currentAveragesDF.loc[0,'precipIn'] = currentAveragesDF.loc[0,'precipIn'] + newWeatherDF.loc[0,'precip']
    #first hour of the day averages being zero is a problem
    if currentAveragesDF.loc[0,'minTempF'] == 0:
        currentAveragesDF.loc[0, 'minTempF'] = newWeatherDF.loc[0,'temp']
    else:
        currentAveragesDF.loc[0,'minTempF'] = min(currentAveragesDF.loc[0,'minTempF'], newWeatherDF.loc[0,'temp'])
    dataObject.storeCurrentWeatherAverages(currentAveragesDF)


def prepDataForModel(dataObject):
    #grab forecast and averages data, create modelDF that will be passed to model
    modelData = dataObject.dfForModel()
    forecastData = dataObject.getForecastAverages()
    currentAverages = dataObject.getCurrentWeatherAverages()
    #hour indicates which row to get forecast data from
    hour = dataObject.getHour()
    if hour != 23:
        modelData.loc[0,'avgtempF'] = (forecastData.loc[hour,'avgTempF'] + currentAverages.loc[0,'avgTempF']) / 24
        modelData.loc[0,'mintempF'] = min(forecastData.loc[hour,'minTempF'], currentAverages.loc[0,'minTempF'])
        modelData.loc[0,'maxtempF'] = max(forecastData.loc[hour,'maxTempF'], currentAverages.loc[0,'maxTempF'])
        modelData.loc[0,'totalprecipIn'] = forecastData.loc[hour,'precipIn'] + currentAverages.loc[0,'precipIn']
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
        today = date.today()
        ordinalIndicator = determineOriginalIndicator(today.day)
        today = today.strftime('%A %b %d')
        todayStatement = "Today - " + str(today) + ordinalIndicator + " Prediction:"
        return todayStatement
    except Exception as e:
        print(f"an error occurred in get_date: {e}")

def get_tomorrow_date():
    try:
        today = date.today()
        tomorrow = today + timedelta(days=1)
        ordinalIndicator = determineOriginalIndicator(tomorrow.day)
        tomorrow = tomorrow.strftime('%A %b %d')
        dateStatement = "Tomorrow - " + str(tomorrow) + ordinalIndicator + " Prediction:"
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