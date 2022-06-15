from django.urls import include, path

from deepcom.controllers.Video.VideoController import VideoController
from . import views



urlpatterns = [
    path('', views.say_hello),
    path('processed-video/', views.processed_video),
    path('video', VideoController())
]


