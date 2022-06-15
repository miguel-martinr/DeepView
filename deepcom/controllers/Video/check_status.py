from deepcom.apps import DeepcomConfig
from deepcom.models import VideoModel


def check_status(video_name):

    video_path = DeepcomConfig.getVideoPath(video_name)
    
    if (VideoModel.objects.filter(video_path=video_path)):
      response = {
          'success': True,
          'message': VideoModel.objects.get(video_path=video_path).status
      }

    else: 
      response = {
          'success': False,
          'message': 'Video not found'
      }
    return response