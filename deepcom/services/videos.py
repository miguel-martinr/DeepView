import os

from deepcom.apps import DeepcomConfig
from deepviewcore.Video import Video

from deepcom.models import VideoModel


class VideoService:
    def __init__(self):
        pass

    def validateVideoFile(filename):
        videos_path = DeepcomConfig.videos_path
        return os.path.isfile(os.path.join(videos_path, filename)) and \
            filename.endswith(DeepcomConfig.allowed_extensions)

    def getAvailableVideos():
        """Gets available videos stats from the videos folder.
        Each video stats is a dictionary with the following keys:
         - name: video name
         - size_in_bytes: video size in bytes
         - duration_in_seconds: video duration in seconds
         - fps: video frames per second
        
        """

        videos_names = []
        for filename in os.listdir(DeepcomConfig.videos_path):
            if VideoService.validateVideoFile(filename):
                videos_names.append(filename)

        videos_stats = []
        for videopath in [os.path.join(DeepcomConfig.videos_path, videoname) for videoname in videos_names]:
            video = Video(videopath)
            current_stats = video.getStats()
            del current_stats['path']
            current_stats['name'] = os.path.basename(videopath)
            # current_stats['status'] = 'UNPROCESSED'            
            videos_stats.append(current_stats)
        return videos_stats

    def processVideo(videoPath):
        """Processes a video and returns the processed video stats.
        """
        if VideoModel.objects.filter(video_path = videoPath):
          print ("Video exists")
        else:
          # Create a new video model
          videoModel = VideoModel(video_path=videoPath, frames=[])
          videoModel.save()
          
          def getParticleData(object):
            return {
              'x': object['circle'][0][0],
              'y': object['circle'][0][1],
              'radius': object['circle'][1],
              'area': object['area'],
            }

          def saveFrameData(objects):
            frame = {
              'particles': [getParticleData(object) for object in objects],
            }
            videoModel.frames.append(frame)
            videoModel.save()
          
          videoCore = Video(videoPath)
          videoModel.status = 'PROCESSING'
          videoModel.save()
          videoCore.process(action=saveFrameData)
          videoModel.status = 'PROCESSED'
          videoModel.save()
          print("Video does not exist")

        
        

        