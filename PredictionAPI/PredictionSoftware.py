from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd

def getFeatures():
    return pd.read_csv("Data/HistoricalData/KNNFeaturesNonScaled.csv")

def getTargetFeature():
    return pd.read_csv("Data/HistoricalData/actualFinalizedSnow.csv")

def getPrediction(todaysWeather):
    #historical features
    features = getFeatures()
    features.reset_index(drop=True, inplace=True)
    #historical target feature 24HourSnow
    targetFeature = getTargetFeature()
    targetFeature = targetFeature['24HourSnow']
    targetFeature.reset_index(drop=True, inplace=True)
    #drop todays weather index
    todaysWeather.reset_index(drop=True, inplace=True)
    #create scalar
    scalar = MinMaxScaler()
    #scale features
    scaledFeaturesDF = scalar.fit_transform(features)
    scaledFeaturesDF = pd.DataFrame(scaledFeaturesDF,columns=features.columns)
    #scale todays weather
    todaysWeatherScaled = scalar.transform(todaysWeather)
    todaysWeatherScaled = pd.DataFrame(todaysWeatherScaled,columns=todaysWeather.columns)
    #KNN_Regressor is the object that is the model
    KNN_Regressor = KNeighborsRegressor(n_neighbors=23,weights='distance',algorithm='ball_tree',p=1)
    #fit it features and target features for the model
    KNN_Regressor.fit(scaledFeaturesDF ,targetFeature)
    #return the prediction
    prediction = KNN_Regressor.predict(todaysWeatherScaled)
    print(todaysWeatherScaled)
    print(prediction)
    return np.rint(prediction[0])