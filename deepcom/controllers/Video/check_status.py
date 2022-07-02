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
    
    if (VideoService.videoExistsInDB(video_path)):
      processed_video = VideoService.getVideoModel(video_path)
      status = processed_video.status

      response = {
          'success': True,
          'message': status
      }

      if (status == 'processing'):
        video_process: Video = VideoService.processes.get(video_path)                


        if (video_process is None):
          VideoService.deleteVideoFromDB(video_path)
          return {
            "success": False,
            "message": "Video status was \"processing\" but no process was found :(. Try processing it again..."
          }


        percentage = int(((video_process.getCurrentFrameIndex() + 1) * 100) / video_process.numOfFrames())
        response["percentage"] = percentage
      
      if (status == 'processed'):
        spent_seconds = processed_video.spent_time
        response['spent_seconds'] = spent_seconds
          

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