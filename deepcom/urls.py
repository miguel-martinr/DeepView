from django.http import HttpRequest
from django.shortcuts import render
from django.urls import path, re_path
from deepcom.controllers.Video.VideoController import VideoController
from . import views


def render_react(request: HttpRequest):
    return render(request, "index.html")


urlpatterns = [    
    path('video', views.video),
    path('videos/<str:video_name>/', views.video_service),
    re_path(r"^(?:.*)/?$", render_react),
]
