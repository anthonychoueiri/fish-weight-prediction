broker: redis-server
scheduler: celery -A PredictionApp beat -l INFO
worker: celery -A PredictionApp worker -l INFO
release: python manage.py migrate
web: gunicorn FishWeightPrediction.wsgi
