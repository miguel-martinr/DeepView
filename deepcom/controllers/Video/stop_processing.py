from deepcom.apps import DeepcomConfig
from deepcom.services.videos import VideoService


def stop_processing(video_name):
    video_path = DeepcomConfig.getVideoPath(video_name)

    if VideoService.stopProcessing(video_path):
        response = {
            "success": True,
            "message": "Video processing stopped"
        }
    else:
        response = {
            "success": False,
            "message": "Video not found"
        }

    return response
