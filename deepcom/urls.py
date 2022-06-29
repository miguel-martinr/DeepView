from django.urls import path, re_path
from django.views.generic.base import RedirectView
from deepcom.controllers.Video.VideoController import VideoController
from . import views



urlpatterns = [
    path('', views.say_hello),
    path('video', views.video),
    path('videos/<str:video_name>/', RedirectView.as_view(url='http://localhost:8000/static/videos/%(video_name)s')),
]


