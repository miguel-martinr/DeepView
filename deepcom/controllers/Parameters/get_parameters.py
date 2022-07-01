from django.http import HttpRequest
from deepcom.apps import DeepcomConfig

from deepcom.services.ParametersService import ParametersService


def get_parameters(request: HttpRequest):
    """
      Returns parameters linked for specific video. If there are no parameters 
      linked for that video it returns the default parameters
    """

    video_name = request.GET.get('video_name')

    if video_name is None:
        return {
            "success": False,
            "message": "No video_name provided"
        }

    video_path = DeepcomConfig.getVideoPath(video_name)
    parameters = ParametersService.getParametersForVideo(video_path)

    return {
        "success": True,
        "parameters": parameters
    }
