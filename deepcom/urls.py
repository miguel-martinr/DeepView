from django.urls import path, re_path
from deepcom.controllers.Video.VideoController import VideoController
from . import views



urlpatterns = [
    path('', views.say_hello),
    path('video', views.video),
    path('videos/<str:video_name>/', views.video_service),
]


