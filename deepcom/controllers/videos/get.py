from django.http import HttpRequest, HttpResponse
from bson.json_util import dumps
from deepcom.services.videos import VideoService

def get_available_videos_controller(request):
  data = VideoService.get_available_videos()
  
  return HttpResponse(dumps(data), content_type='application/json')