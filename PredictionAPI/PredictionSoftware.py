from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd

def getFeatures():
    return pd.read_csv("kNNReadyScaledFeatures.csv")

def getTargetFeature():
    return pd.read_csv("finalizedSnow.csv")

def getPrediction(todaysWeather):
    #historical features
    features = getFeatures()
    #historical target feature 24HourSnow
    targetFeature = getTargetFeature()
    #create scalar
    scalar = MinMaxScaler()
    #scale todays weather
    todaysWeatherScaled = scalar.fit_transform(todaysWeather)
    #KNN_Regressor is the object that is the model
    KNN_Regressor = KNeighborsRegressor(n_neighbors=23,weights='distance',algorithm='ball_tree',p=1)
    #fit it features and target features for the model
    KNN_Regressor.fit(features,targetFeature)
    #return the prediction
    prediction = KNN_Regressor.predict(todaysWeatherScaled)

    return np.rint(prediction)
