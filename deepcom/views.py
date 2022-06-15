


from django.http import HttpResponse
from django.shortcuts import render
from deepcom.controllers.process_video.process import process_video_controller




from deepcom.controllers.processed_video.get import get_processed_video_controller
from deepcom.controllers.videos.check_status import check_status_controller
from deepcom.controllers.videos.get_available import get_available_videos_controller

from deepcom.models import ParticleData, VideoModel





# Hello
def say_hello(request):

    return render(request, 'hello.html', {
        'name': 'Miguel',
    })


# Processed video
def processed_video(request):
  if request.method == 'GET':
    return get_processed_video_controller(request)
  else:
    return HttpResponse(status=404)


# Videos
def available_videos(request):
  if request.method == 'GET':
    return get_available_videos_controller(request)
  else:
    return HttpResponse(status=404)


def process_video(request):
  if request.method == 'POST':
    return process_video_controller(request)

def check_status(request):
  if request.method == 'GET':
    return check_status_controller(request)
  else:
    return HttpResponse(status=404)
    


