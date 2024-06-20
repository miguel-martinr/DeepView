from django.http import HttpRequest, HttpResponse
from bson.json_util import dumps
from deepcom.services.VideoService import VideoService

def list_available(request):
  list = VideoService.get_all_available_video_data()
  response = {
    "success": True,
    "message": list,
  }
  return response