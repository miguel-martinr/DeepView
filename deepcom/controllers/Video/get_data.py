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

    
    unit = request.GET.get('unit')
    if unit is None:
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

    try:
      partciles_by_time_unit = VideoService.getParticlesByTimeUnit(video_path, unit)
      seconds_with_events = VideoService.getSecondsWithEvents(video_path)
      events = VideoService.getEvents(video_path)

    except Exception as e:
      return {
        "success": False,
        "message": str(e)
      }

    response["data"] = {

      # Particles
      "particles": {
        "by_time_unit": partciles_by_time_unit,
        "time_unit": unit
      },
      
      # Events
      "events": {
        "seconds_with_events": seconds_with_events,
        "events": events,
      }
    }
    
    return response
