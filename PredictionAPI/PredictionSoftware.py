from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from imblearn.over_sampling import SMOTE
import numpy as np
import pandas as pd


def getFeatures():
    return pd.read_csv("Data/HistoricalData/KNNFeaturesNonScaled.csv")


def getTargetFeature():
    return pd.read_csv("Data/HistoricalData/actualFinalizedSnow.csv")


class SnowPredictor:
    def __init__(self):
        self.bins = []
        self.scalar = None
        self.model = None
        self.fitScalarAndModel()

    def fitScalarAndModel(self):
        features = getFeatures()
        targetFeature = getTargetFeature()
        targetFeature.loc[targetFeature['24HourSnow'] > 20, '24HourSnow'] = 20
        bins = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
        self.bins = bins
        target_binned = pd.cut(
            targetFeature['24HourSnow'],
            bins=bins,
            labels=False,
            include_lowest=True,
            right=True
        )
        target_binned = np.where(targetFeature['24HourSnow'] == 0, 0, target_binned + 1)
        smote = SMOTE(random_state=42)
        X_smote, y_smote = smote.fit_resample(features, target_binned)
        self.scalar = StandardScaler()
        scaledSmoteFeatures = self.scalar.fit_transform(X_smote)
        clf = MLPClassifier(
            hidden_layer_sizes=(400, 350, 300, 250),
            activation='relu',
            solver='adam',
            batch_size=55,
            learning_rate='adaptive',
            random_state=1,
            max_iter=10000,
            learning_rate_init=0.0009,
            early_stopping=True,
            alpha=0.001,
            momentum=0.9
        )
        clf.fit(scaledSmoteFeatures, y_smote)
        self.model = clf

    def makePrediction(self, todaysWeather):
        todaysWeatherScaled = self.scalar.transform(todaysWeather)
        prediction = self.model.predict(todaysWeatherScaled)
        return self.binPrediction(prediction)

    def binPrediction(self, binIndex):
        bins = self.bins
        if 0 <= binIndex < len(bins):
            if binIndex == 0:
                return "0"
            else:
                return f"{bins[binIndex - 1]}-{bins[binIndex]}"
        else:
            return f"Overflow{binIndex}"

    '''OLD PREDICTION METHOD

    def getPrediction(self, todaysWeather):
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
        return np.rint(prediction[0])'''
