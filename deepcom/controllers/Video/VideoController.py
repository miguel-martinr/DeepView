import json
from django.http import HttpRequest, HttpResponse



from .get_data import get_data
from .list_available import list_available
from .check_status import check_status
from .process import process_video
from .stop_processing import stop_processing
from .process_frame import process_frame


class VideoController:
    post_actions = {
        "stop": stop_processing,
        "process": process_video,
        "process_frame": process_frame,        
    }

    get_actions = {
        "check-status": check_status,
        "list-available": list_available,
        "get-data": get_data,        
    }

    def __init__(self):
        pass

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'POST':
            response = VideoController.handlePostRequest(request)
        elif request.method == 'GET':
            response = VideoController.handleGetRequest(request)
        else:
            return HttpResponse(status=400)

        return HttpResponse(json.dumps(response), content_type='application/json')

    def handlePostRequest(request):
        body = VideoController.parseRequestBody(request.body)
        if not body['action']:
            response = {
                "success": False,
                "message": "No action provided"
            }
            return response

        if not body['action'] in VideoController.post_actions:
            response = {
                "success": False,
                "message": f"Action {body['action']} not found"
            }
            return response

        action = body['action']
        payload = body['payload']

        # print("##################", action, payload)
        response = VideoController.post(action, payload)
        return response

    def parseRequestBody(body: bytes):
        decoded_body = body.decode('utf-8')
        json_body = json.loads(decoded_body)
        return json_body

    def handleGetRequest(request):
        action = request.GET.get('action')
        if not action:
            response = {
                "success": False,
                "message": "No action provided"
            }
            return response

        if not action in VideoController.get_actions:
            response = {
                "success": False,
                "message": f"Action {action} not found"
            }
            return response

        response = VideoController.get(action, request)
        return response

    def post(action, payload):
        return VideoController.post_actions[action](payload)

    def get(action, payload):
        return VideoController.get_actions[action](payload)
