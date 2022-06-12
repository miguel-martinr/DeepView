from djongo import models
from django import forms


class ParticleData(models.Model):
  x = models.FloatField()
  y = models.FloatField()
  radius = models.FloatField()
  area = models.FloatField()
  class Meta:
    abstract = True

class ParticleDataForm(forms.ModelForm):
  class Meta:
    model = ParticleData
    fields = ('x', 'y', 'radius', 'area')


class ProcessedVideo(models.Model):
  _id = models.ObjectIdField()
  created_at = models.DateTimeField()
  video_path = models.CharField(max_length=255)

  data = models.ArrayField(
    model_container=ParticleData,
    model_form_class=ParticleDataForm,
  )

  objects = models.DjongoManager()
