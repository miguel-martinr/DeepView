
from djongo import models
from django import forms


class TopHatParameters(models.Model):
    kernelWidth = models.IntegerField()
    kernelHeight = models.IntegerField()

    class Meta:
        abstract = True


class PreprocessParameters(models.Model):
    top_hat = models.EmbeddedField(
        model_container=TopHatParameters
    )

    class Meta:
        abstract = True



