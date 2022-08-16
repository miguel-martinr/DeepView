from djongo import models
from django import forms

from deepcom.apps import DeepcomConfig

from .custom_models.processing_parameters import EventsParameters, PreprocessParameters, ProcessParameters



class Second(models.Model):
    mode = models.IntegerField(null=False)

    class Meta:
        abstract = True

class VideoModel(models.Model):
    _id = models.ObjectIdField()
    created_at = models.DateTimeField(auto_now_add=True)

    video_path = models.CharField(max_length=255)
    status = models.CharField(default='unprocessed', max_length=255)

    by_second = models.ArrayField(
      model_container=Second
    )

    spent_time = models.FloatField(null=True)

    objects = models.DjongoManager()

class ProcessingParametersModel(models.Model):  
  preprocess = models.EmbeddedField(
      model_container=PreprocessParameters,
      null=False,
      default = DeepcomConfig.default_preprocess_parameters
  )

  process = models.EmbeddedField(
    model_container=ProcessParameters,
    null=False,
    default = DeepcomConfig.default_process_parameters
  )

  events = models.EmbeddedField(
    model_container=EventsParameters,
    null=False,
    default = DeepcomConfig.default_events_parameters
  )

  video_linked = models.CharField(max_length=255, null=False, unique=True)
  objects = models.DjongoManager()

