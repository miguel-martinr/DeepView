import mimetypes
import os
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from ranged_response import RangedFileResponse
from DeepView.settings import STATIC_URL
from deepcom.apps import DeepcomConfig
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import RedirectView
from deepcom.controllers.Video.VideoController import VideoController




@csrf_exempt
def video(request):
  controller = VideoController()
  return controller(request) 


def video_service(request: HttpRequest, video_name):
  host = request.get_host()
  fullpath = "http://" + host + '/' + STATIC_URL + 'videos/' + video_name
  print("####PATH")
  print(fullpath)

  return RedirectView.as_view(url=fullpath)(request)


    


