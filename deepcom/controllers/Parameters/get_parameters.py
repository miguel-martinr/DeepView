from django.http import HttpRequest


def get_parameters(request: HttpRequest):

    return {
        "success": True,
        "message": "Testing"
    }
