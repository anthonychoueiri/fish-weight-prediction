worker.1: redis-server
worker.2: celery -A PredictionApp beat -l INFO
worker.3: celery -A PredictionApp worker -l INFO
web: gunicorn FishWeightPrediction.wsgi
