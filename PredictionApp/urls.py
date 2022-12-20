from django.urls import path

from . import views

urlpatterns = [
    path('predict', views.predict, name='predict'),
    path('add', views.add, name='add'),
    path('train', views.trigger_training, name='trigger_training'),
]
