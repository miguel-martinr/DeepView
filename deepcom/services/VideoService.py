import os
from deepcom.apps import DeepcomConfig
from deepviewcore.Video import Video
import threading
from deepcom.models import VideoModel
from deepcom.services.ParametersService import ParametersService
from deepcom.services.utils import get_particles_by_second, get_particles_quantity, segment
from django.utils import timezone

class VideoService:
    processes = {}
    lock = threading.Lock()

    def __init__(self):
        pass

    def videoExistsInDB(videoPath=None, videoName=None):
        if videoPath is not None:
            path = videoPath
        elif videoName is not None:
            path = DeepcomConfig.getVideoPath(videoName)
        else:
            return False

        documents = VideoModel.objects.filter(video_path=path)
        return len(documents) > 0

    def getVideoModel(videoPath=None, videoName=None):
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
        else:
            return False

    def processVideo(videoPath):
        """Processes a video and returns the processed video stats.
        """
        if VideoService.videoExistsInDB(videoPath):
            print(f"Video processed exists in database. Removing {videoPath}...")
            VideoModel.objects.filter(video_path=videoPath).delete()
        else:
            print(f"Video processed does not exist. Adding {videoPath}...")


        # Create a new video model
        videoModel = VideoModel(
          video_path=videoPath, 
          by_second=[], 
          seconds_with_events=[])
          
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
                
        
        def saveData(results):
            frames, events = results
            formatted_frames = []
            for cur_frame in frames:
                frame = {
                    'particles': [getParticleData(object) for object in cur_frame],
                }
                formatted_frames.append(frame)

            by_second = [{"mode": mode}
                          for mode in get_particles_by_second(formatted_frames)]

            videoModel.by_second.extend(by_second)
            videoModel.seconds_with_events.extend([{"second": key} for key in events.keys()])            
            videoModel.save()

        def process():
            videoModel.status = 'processing'
            videoModel.save()

            # Save each 2010 frames (67 seconds of video)
            videoCore.frame_interval = 2010
            videoCore.process(
                action=saveData, 
                showContours=False, 
                options=options)
            del VideoService.processes[videoPath]

            ret, _ = videoCore.cap.read()
            if not ret and videoCore.keep_processing:
                videoModel.status = 'processed'
            else:
                videoModel.status = 'stopped'
                videoCore.setFrameIndex(
                    videoCore.getCurrentFrameIndex() - 1)

            now = timezone.now()
                 
            videoModel.spent_time = (now - videoModel.created_at).total_seconds()

            
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

    def getParticlesBySecond(videoPath: str):
        if not VideoService.videoExistsInDB(videoPath):
            raise Exception(f"Couldn't get particles by second because <{videoPath}> video doesn't exist")

        model: VideoModel = VideoService.getVideoModel(videoPath)
        by_second = [second['mode'] for second in model.by_second]
        return by_second

    def getSecondsWithEvents(videoPath: str):
        if not VideoService.videoExistsInDB(videoPath):
            raise Exception(f"Couldn't get seconds with events because video <{videoPath}> doesn't exist")
        
        model: VideoModel = VideoService.getVideoModel(videoPath)
        seconds_with_events = [second['second'] for second in model.seconds_with_events]
        return seconds_with_events


    def getParticlesByTimeUnit(videoPath: str, unit: str):
        by_second = VideoService.getParticlesBySecond(videoPath)
        if unit == 'seconds':
            return by_second

        elif unit == 'minutes':
            group_size = 60

        else:
            group_size = 3600

        return [sum(segment) for segment in segment(by_second, group_size)]

    def deleteVideoFromDB(videoPath: str):
        VideoModel.objects.filter(video_path=videoPath).delete()