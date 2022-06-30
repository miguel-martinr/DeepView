import os

from deepcom.apps import DeepcomConfig
from deepviewcore.Video import Video
import threading
from deepcom.models import VideoModel
from deepcom.services.ParametersService import ParametersService


class VideoService:
    processes = {}
    lock = threading.Lock()

    def __init__(self):
        pass

    def videoExistsInDB(videoPath = None, videoName = None):
      if videoPath is not None:
        path = videoPath
      elif videoName is not None:
        path = DeepcomConfig.getVideoPath(videoName)
      else:
        return False

      documents = VideoModel.objects.filter(video_path=path)
      return len(documents) > 0

    def getVideoModel(videoPath = None, videoName = None):
      if videoPath is not None:
        path = videoPath
      elif videoName is not None:
        path = DeepcomConfig.getVideoPath(videoName)
      else:
        return False

      return VideoModel.objects.get(video_path=path)

    def validateVideoFile(filename):
        videos_path = DeepcomConfig.videos_path
        return os.path.isfile(os.path.join(videos_path, filename)) and \
            filename.endswith(DeepcomConfig.allowed_extensions)

    def getAvailableVideos():
        """Gets available videos stats from the videos folder.
        Each video stats is a dictionary with the following keys:
         - name: video name
         - size_in_MB: video size in MB
         - duration_in_seconds: video duration in seconds
         - fps: video frames per second
         - status: video status. (processing, processed, stopped, unprocessed)

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
            
            if (not VideoModel.objects.filter(video_path=videopath)):
                current_stats['status'] = 'unprocessed'
            else:
                videoModel = VideoModel.objects.get(video_path=videopath)
                current_stats['status'] = videoModel.status

            # current_stats['status'] = 'UNPROCESSED'
            videos_stats.append(current_stats)
        return videos_stats

    def stopProcessing(videoPath):
        if videoPath in VideoService.processes:
            with VideoService.lock:
                video: Video = VideoService.processes[videoPath]
                video.stop_processing()
                return True
            # TODO: check if process is complete
        else:
            return False

    def processVideo(videoPath):
        """Processes a video and returns the processed video stats.
        """
        if VideoService.videoExistsInDB(videoPath):
            print("Video exists. Skipping process...")
        else:
            print("Video does not exist. Adding it...")
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

            videoCore = Video(videoPath)

            # Get processing parameters
            options = ParametersService.getParametersForVideo(videoPath)
            print(f"##### OPTIONS: {options}")

            def saveData(frames):            
                for cur_frame in frames:                  
                  frame = {
                      'particles': [getParticleData(object) for object in cur_frame],
                  }
                  videoModel.frames.append(frame)                
                videoModel.save()
                

            def process():
                videoModel.status = 'processing'
                videoModel.save()

                videoCore.frame_interval = 2000 # Save each 2000 frames
                videoCore.process(action=saveData, showContours=False, options=options)
                del VideoService.processes[videoPath]
                
                if videoCore.numOfFrames() == len(videoModel.frames):
                  videoModel.status = 'processed'
                else:
                  videoModel.status = 'stopped'

                videoModel.save()
                print(
                    f"THREAD FINISHED VideoService.processes--> {VideoService.processes.__str__()}")

            VideoService.processes[videoPath] = videoCore
            new_thread = threading.Thread(target=process)
            new_thread.start()


    def processFrame(videoPath, frameIndex, params):
        video = Video(videoPath)
        video.setFrameIndex(frameIndex)
        return video.processFrame(options=params)
        