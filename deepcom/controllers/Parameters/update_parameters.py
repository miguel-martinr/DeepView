from deepcom.apps import DeepcomConfig
from deepcom.controllers.Parameters.utils import printExceptionMessage
from deepcom.services.ParametersService import ParametersService


def update_parameters(payload):

    parameters = payload.get("parameters")
    if parameters is None:
        return {
            "success": False,
            "message": "No parameters provided"
        }

    video_name = payload.get("video_name")

    if video_name is None:
        return {
            "success": False,
            "message": "No video name provided"
        }

    video_path = DeepcomConfig.getVideoPath(video_name)

    try:
        ParametersService.updateParameters(
            video_path=video_path, parameters=parameters)

    except Exception as e:

        return {
            "success": False,
            "message": f"{printExceptionMessage(e)}"
        }

    return {
        "success": True,
        "message": "Parameters updated"
    }
