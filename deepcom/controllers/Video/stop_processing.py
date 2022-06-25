from deepcom.apps import DeepcomConfig
from deepcom.models import VideoModel
from deepcom.services.videos import VideoService


def stop_processing(video_name):
    video_path = DeepcomConfig.getVideoPath(video_name)

    if VideoService.stopProcessing(video_path):
        response = {
            "success": True,
            "message": "Video processing stopped"
        }
    elif (VideoModel.objects.filter(video_path)):
      status = VideoModel.objects.get(video_path=video_path).status
      response = {
        "sucess": True,
        "message": f"Video is not processing. Current status: {status}"
      }
    else:
        response = {
            "success": False,
            "message": "Video not found"
        }

    return response
