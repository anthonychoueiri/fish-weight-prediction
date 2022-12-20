import os
from celery import Celery
import pandas as pd
from PredictionApp.inference import PredictionModel, DF_TRAIN_PATH, PICKLE_PATH


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FishWeightPrediction.settings")
app = Celery("FishWeightPrediction")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task()
def train():
    print('training model')

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
