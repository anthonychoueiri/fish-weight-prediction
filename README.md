# Fish Weight Prediction

A machine learning model that predicts fish weight exposed on a REST API.

Deployed on https://fish-weight-prediction-api.herokuapp.com.

## Table of Contents

1. [Overview](#overview)
2. [Description](#description)
3. [Setup](#setup)
4. [Documentation](#documentation)

## Overview

The system is a REST API that predicts fish weight based on 6 variables:
- **Species**: species name of fish
- **Length1**: vertical length in cm
- **Length2**: diagonal length in cm
- **Length3**: cross length in cm
- **Height**: height in cm
- **Width**: width in cm

It has the following features:
- Scheduled re-training of the model
- Ability to add new data to the dataset
- Manually triggering re-training of the model

The [Fish market](https://www.kaggle.com/datasets/aungpyaeap/fish-market?datasetId=229906) dataset is used to train the model.

## Description

The system is a Django web application deployed on Heroku. It uses Celery to schedule a worker task every 10 minutes that re-trains the model, with Redis as the message broker.

The Django project `FishWeightPrediction` has a single app `PredictionApp` where most of the logic is located. It has 3 paths:
- `/predict`: returns a fish weight prediction based on 6 query parameters
- `/add`: used to add new fish data to the dataset
- `/train`: triggers a training for the model

When running the system locally, the message broker used is Redis Server. On the Heroku deployment, it's the Redis Cloud add-on.

## Setup

The web app is deployed on https://fish-weight-prediction-api.herokuapp.com, but it can be setup locally as well.

The first step is to install the required packages with `pip`:
```
pip install -r requirements.txt
```
Then, you need to create and apply migrations:
```
python manage.py makemigrations
python manage.py migrate
```
Finally, you need to run four processes:
1. Redis Server: `redis-server`
2. Celery beat: `celery -A PredictionApp beat -l INFO`
3. Celery worker: `celery -A PredictionApp worker -l INFO -E`
4. The Django web app: `python manage.py runserver`

## Documentation

### Fish weight prediction

Returns the fish weight predicted by the ML model.

This API needs 6 variables passed in the request to compute the prediction.

- **Path**: `/predict`
- **HTTP method**: `GET`
- **_Returns_**: JSON response that includes the predicted weight (`integer`) and the 6 variables passed in the request

#### Data:
The 6 variables should be passed as query parameters.
|Parameter|Type|
|---|---|
|`species`|`string`, should be one of `Bream`, `Roach`, `Whitefish`, `Parkki`, `Perch`, `Pike`, `Smelt`|
|`length1`|`float`|
|`length2`|`float`|
|`length3`|`float`|
|`height`|`float`|
|`width`|`float`|

### Adding new fish data to dataset

Appends new row containing fish data to the dataset CSV file.

This API needs all 7 variables passed in the body of the request.

- **Path**: `/add`
- **HTTP method**: `POST`
- **_Returns_**: `Added to dataset` response

#### Data:
The 7 variables should be passed in the body of the request as `x-www-form-urlencoded`.
|Parameter|Type|
|---|---|
|`species`|`string`, should be one of `Bream`, `Roach`, `Whitefish`, `Parkki`, `Perch`, `Pike`, `Smelt`|
|`length1`|`float`|
|`length2`|`float`|
|`length3`|`float`|
|`height`|`float`|
|`width`|`float`|
|`weight`|`integer`|

### Trigger model training

Manually triggers the training of the machine learning model and saves it.

This API doesn't need any data to be passed in the request.

-- **Path**: `/train`
- **HTTP method**: `POST`
- **_Returns_**: `Training complete, model saved` response
