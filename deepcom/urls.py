from django.urls import include, path

from deepcom.controllers.Video.VideoController import VideoController
from . import views



urlpatterns = [
    path('', views.say_hello),
    path('processed-video/', views.processed_video),
    path('available-videos/', views.available_videos),
    # path('process-video/', views.process_video),
    path('check-status/', views.check_status),
    path('video', VideoController())
]


