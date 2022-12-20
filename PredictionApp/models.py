from django.db import models


class Fish(models.Model):
    species = models.CharField(max_length=100)
    length1 = models.FloatField()
    length2 = models.FloatField()
    length3 = models.FloatField()
    height = models.FloatField()
    width = models.FloatField()
    weight = models.IntegerField()
