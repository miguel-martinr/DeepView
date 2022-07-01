import json
from django.http import HttpRequest, HttpResponse

from deepcom.controllers.Parameters.add_parameters import add_parameters
from deepcom.controllers.Parameters.get_parameters import get_parameters


class ParametersController:
    post_actions = {
        "add": add_parameters,
    }

    get_actions = {
        "get-parameters-for-video": get_parameters,
    }

    def __init__(self):
        pass

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'POST':
            response = ParametersController.handlePostRequest(request)
        elif request.method == 'GET':
            response = ParametersController.handleGetRequest(request)
        else:
            return HttpResponse(status=400)

        return HttpResponse(json.dumps(response), content_type='application/json')

    def handlePostRequest(request):
        body = ParametersController.parseRequestBody(request.body)
        if not body['action']:
            response = {
                "success": False,
                "message": "No action provided"
            }
            return response

        if not body['action'] in ParametersController.post_actions:
            response = {
                "success": False,
                "message": f"Action {body['action']} not found"
            }
            return response

        action = body['action']
        payload = body['payload']

        # print("##################", action, payload)
        response = ParametersController.post(action, payload)
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

        if not action in ParametersController.get_actions:
            response = {
                "success": False,
                "message": f"Action {action} not found"
            }
            return response

        response = ParametersController.get(action, request)
        return response

    def post(action, payload):
        return ParametersController.post_actions[action](payload)

    def get(action, payload):
        return ParametersController.get_actions[action](payload)
