
from deepcom.apps import DeepcomConfig
from deepcom.services.videos import VideoService

def process_video(video_name):
    video_path = DeepcomConfig.getVideoPath(video_name)

    VideoService.processVideo(video_path)
    response = {
      'success': True,
      'message': 'Video is being processed'
    }

    return response