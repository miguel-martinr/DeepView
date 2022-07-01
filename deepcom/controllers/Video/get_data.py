from django.http import HttpRequest
from deepcom.apps import DeepcomConfig
from deepcom.models import VideoModel
from deepcom.services.VideoService import VideoService
from deepcom.services.utils import get_particles_quantity, summarize




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
        unit = request.GET.get('unit')
    except KeyError:
        unit = 'minutes'
    
    if not unit in ['seconds', 'minutes', 'hours']:
      return {
        "success": False,
        "message": f"Unit {unit} not supported"
      }

    response = {
        'success': True,
    }

    video_path = DeepcomConfig.getVideoPath(video_name)
    if not VideoService.videoExistsInDB(video_path):
        return {
            'success': False,
            'message': 'Video not found',
        }

    
    by_second = VideoService.getParticlesBySecond(video_path)

    getters = {
      'seconds': lambda: by_second,
      'minutes': lambda: summarize(by_second, 60),
      'hours': lambda: summarize(by_second, 3600)
    }
    response["data"] = getters[unit]()
    return response
