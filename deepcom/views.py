import mimetypes
import os
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from ranged_response import RangedFileResponse
from deepcom.apps import DeepcomConfig
from django.views.decorators.csrf import csrf_exempt

from deepcom.controllers.Video.VideoController import VideoController





# Hello
def say_hello(request):
    return render(request, 'hello.html', {
        'name': 'Miguel',
    })




@csrf_exempt
def video(request):
  controller = VideoController()
  return controller(request)


    


