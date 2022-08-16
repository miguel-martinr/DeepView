
from djongo import models
from django import forms


class TopHatParameters(models.Model):
    kernelWidth = models.IntegerField()
    kernelHeight = models.IntegerField()

    class Meta:
        abstract = True

class ThresholdParameters(models.Model):
    thresh = models.IntegerField()

    class Meta:
        abstract = True

class PreprocessParameters(models.Model):
    top_hat = models.EmbeddedField(
        model_container=TopHatParameters
    )

    class Meta:
        abstract = True

class ProcessParameters(models.Model):
    threshold = models.EmbeddedField(
      model_container=ThresholdParameters
    )

    class Meta:
        abstract = True

class EventsParameters(models.Model):
    minArea = models.IntegerField()

    class Meta:
        abstract = True


