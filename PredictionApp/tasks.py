from celery import shared_task
import pandas as pd
from .inference import PredictionModel, DF_TRAIN_PATH, PICKLE_PATH


def train():
    print('training')
    # model setup
    model = PredictionModel()

    # training of the model
    train_df = pd.read_csv(DF_TRAIN_PATH)
    model.train(train_df)

    # model serialization
    model.serialize(PICKLE_PATH)

    # clearing up
    del model
    print('done')
