from djongo import models


class EventModel(models.Model):
  frame_index = models.IntegerField()
  x = models.FloatField()
  y = models.FloatField()
  radius = models.FloatField()
  area = models.FloatField()

  class Meta:
    abstract = True