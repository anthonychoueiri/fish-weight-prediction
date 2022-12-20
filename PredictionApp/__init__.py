from FishWeightPrediction.celery import app as celery_app
from .tasks import train

__all__ = ("celery_app",)
