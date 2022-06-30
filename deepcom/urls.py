from django.urls import path
from deepcom.controllers.Video.VideoController import VideoController
from . import views




urlpatterns = [    
    path('video', views.video),
    path('parameters', views.parameters),
    path('videos/<str:video_name>/', views.video_service),
]
