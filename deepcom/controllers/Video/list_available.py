from django.http import HttpRequest, HttpResponse
from bson.json_util import dumps
from deepcom.services.VideoService import VideoService

def list_available(request):
  list = VideoService.getAvailableVideos()
  response = {
    "success": True,
    "message": list,
  }
  return response