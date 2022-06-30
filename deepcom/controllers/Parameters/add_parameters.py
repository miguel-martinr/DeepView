from deepcom.apps import DeepcomConfig
from deepcom.services.ParametersService import ParametersService


def add_parameters(payload):
  
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

  ParametersService.saveParameters(video_path=video_path, parameters=parameters)
  
  return {
    "success": True,
    "message": "Parameters added"
  }