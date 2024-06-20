from deepcom.apps import DeepcomConfig
from deepcom.services.ParametersService import ParametersService


from deepcom.services.VideoService import VideoService


def process_frame(payload):
  # Get video name
  video_name = payload.get('video_name')
  
  if video_name is None:
    return {
      "sucess": False,
      "message": "No video name provided"
    }

  # Get processing parameters
  params = payload.get('params')

  if params is None:
    return {
      "sucess": False,
      "message": "No processing parameters provided"
    }
  

  # Get frame index
  frame_index = payload.get('frame_index')
  
  if frame_index is None:
    return {
      "success": False,
      "message": "No frame index provided"
    }

    

  if (not VideoService.validate_video_file(video_name)):
    return {
      "success": False,
      "message": "Video not found",
    }

  # Form video path
  videoPath = DeepcomConfig.getVideoPath(video_name)  
  params = ParametersService.formatParameters(params)
  
  objects = VideoService.processFrame(videoPath, frame_index, params)[1]
  return {
    "success": True,
    "result": list(objects)
  }
  
