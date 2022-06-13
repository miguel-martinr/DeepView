import json
from os import path
from django.http import HttpRequest, HttpResponse
from deepcom.apps import DeepcomConfig

from deepcom.models import VideoModel


def check_status_controller(request: HttpRequest):
    video_name = request.GET.get('video_name')
    video_path = path.join(DeepcomConfig.videos_path, video_name)
    
    if (VideoModel.objects.filter(video_path=video_path)):
      response = {
          'success': True,
          'status': VideoModel.objects.get(video_path=video_path).status
      }
    else: 
      response = {
          'success': False,
          'message': 'Video not found'
      }
    return HttpResponse(json.dumps(response))