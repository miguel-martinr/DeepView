import json
from django.http import HttpRequest, HttpResponse

from .process import process_video
from .stop_processing import stop_processing


class VideoController:
    actions = {
        "stop": stop_processing,
        "process": process_video
    }

    def __init__(self):
        pass

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'POST':
            response = VideoController.handlePostRequest(request)
            return HttpResponse(json.dumps(response), content_type='application/json')
        else:
            return HttpResponse(status=400)

    def handlePostRequest(request):
        body = VideoController.parseRequestBody(request.body)
        if not body['action']:
            response = {
                "success": False,
                "message": "No action provided"
            }
            return response

        if not body['action'] in VideoController.actions:
            response = {
                "success": False,
                "message": f"Action {body['action']} not found"
            }
            return response

        action = body['action']
        payload = body['payload']

        print(action, payload)
        response = VideoController.post(action, payload)
        return response

    def parseRequestBody(body: bytes):
        decoded_body = body.decode('utf-8')
        json_body = json.loads(decoded_body)
        return json_body

    def post(action, payload):
        return VideoController.actions[action](payload)
