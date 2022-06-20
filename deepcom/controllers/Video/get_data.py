import json
from django.http import HttpRequest
from deepcom.apps import DeepcomConfig
from deepcom.models import VideoModel


def get_data(request: HttpRequest):
    """
    Get data from the video.
    """
    try:
        video_name = request.GET.get('video_name')
    except KeyError:
        return {
            'success': False,
            'message': 'No video name provided',
        }

    try:
        params = request.GET.get('params')
    except KeyError:
        return {
            'success': False,
            'message': 'No video name provided',
        }

    video_path = DeepcomConfig.getVideoPath(video_name)

    if len(VideoModel.objects.filter(video_path=video_path)) == 0:
        return {
            'success': False,
            'message': 'Video not found',
        }

    video_model: VideoModel = VideoModel.objects.get(video_path=video_path)

    response = {"success": True}
    response["message"] = {
        "frames": video_model.frames
    }

    return response
