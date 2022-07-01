from deepcom.apps import DeepcomConfig
from deepcom.models import VideoModel
from deepcom.services.VideoService import VideoService
from deepviewcore.Video import Video

def check_status(request):

    video_name = request.GET.get('video_name')
    if not video_name:
        return {
            'success': False,
            'message': 'No video name provided',
        }
        
    video_path = DeepcomConfig.getVideoPath(video_name)
    
    if (VideoModel.objects.filter(video_path=video_path)):
      status = VideoModel.objects.get(video_path=video_path).status
      response = {
          'success': True,
          'message': status
      }

      if (status == 'processing'):
        video_process: Video = VideoService.processes.get(video_path)                
        percentage = int(((video_process.getCurrentFrameIndex() + 1) * 100) / video_process.numOfFrames())
        response["percentage"] = percentage
          

    elif (VideoService.validateVideoFile(video_name)): 
      response = {
          'success': True,
          'message': 'unprocessed'
      }

    else:
      response = {
          'success': False,
          'message': 'Video not found'
      }


    return response