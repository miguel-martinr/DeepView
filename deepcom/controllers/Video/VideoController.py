import json
from django.http import HttpRequest, HttpResponse
from .stop_processing import stop_processing



class VideoController:
  actions = {
    "stop": stop_processing,
  }

  def __init__(self):
    pass

  def __call__(self, request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
      action = request.GET.get('action')
      payload = request.GET.get('payload')
      print(action, payload)
      response = VideoController.post(action, payload)
      return HttpResponse(json.dumps(response), content_type='application/json')
    else: 
      return HttpResponse(status=403)


  def post(action, payload):
    return VideoController.actions[action](payload)



  