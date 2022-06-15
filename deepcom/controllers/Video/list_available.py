from django.http import HttpRequest, HttpResponse
from bson.json_util import dumps
from deepcom.services.videos import VideoService

def list_available(payload):
  list = VideoService.getAvailableVideos()
  response = {
    "success": True,
    "message": list,
  }
  return response