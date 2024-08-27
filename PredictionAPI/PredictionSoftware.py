from sklearn.neighbors import KNeighborsRegressor
import pandas as pd

def getFeatures():
    return pd.read_csv("kNNReadyScaledFeatures.csv")

def getTargetFeature():
    return pd.read_csv("finalizedSnow.csv")

def getPrediction(todaysWeather):
    features = getFeatures()
    targetFeature = getTargetFeature()
    #KNN_Regressor is the object that is the model
    KNN_Regressor = KNeighborsRegressor(n_neighbors=23,weights='distance',algorithm='ball_tree',p=1)
    #fit it features and target features for the model
    KNN_Regressor.fit(features,targetFeature)
    #return the prediction
    return KNN_Regressor.predict(todaysWeather)
