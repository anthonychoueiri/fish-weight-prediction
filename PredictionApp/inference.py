import os
import pickle
import pandas as pd


#Prediction Model definition
class PredictionModel:
    def __init__(self, encoder=None, model=None):
        import pickle
        self.encoder = encoder
        self.model = model
        
    #predicts fish weight based on parameters
    def predict(self, 
                species: str, 
                vertical_length: float,
                diagonal_length: float,
                cross_length: float,
                height: float,
                width: float
               ) -> float:
        import numpy as np
        
        if self.model is None:
            raise Exception("Model wasn't trained")
        
        enc = np.array([species]).reshape(-1, 1)
        encoded_part = self.encoder.transform(enc).toarray()
        X = np.hstack([
            np.array([vertical_length, diagonal_length, cross_length, height, width]).reshape(1, 5), 
            encoded_part
        ])
        
        return self.model.predict(X)
    
    # trains new model using pandas dataframe
    # dataframe structure should replicate fish_train.csv structure
    def train(self, df: pd.DataFrame) -> None:
        from sklearn.linear_model import LinearRegression
        from sklearn.preprocessing import OneHotEncoder
        import numpy as np
        
        self.encoder = OneHotEncoder()
        encoded_part = self.encoder.fit_transform(df.Species.values.reshape(-1, 1)).toarray()
        
        y = df.Weight.values
        X = df.drop(['Species', 'Weight'], axis=1)
        X = np.hstack([X.values, encoded_part])
        
        self.model = LinearRegression()
        self.model.fit(X, y)
    
    # creates new pickle file
    def serialize(self, path: str) -> None:
        import pickle
        with open(path, 'wb') as out:
            pickle.dump(self, out, pickle.HIGHEST_PROTOCOL)


def create_path(filename: str):
    relative_path = 'PredictionApp/' + filename
    return os.path.join(os.getcwd(), relative_path)


DF_TRAIN_PATH = create_path('fish_train.csv')
PICKLE_PATH = create_path('v1.model')
