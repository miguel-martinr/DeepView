from django.urls import path

from deepcom.controllers.Video.VideoController import VideoController
from . import views



urlpatterns = [
    path('', views.say_hello),
    path('video', VideoController())
]


