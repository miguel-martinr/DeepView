from asyncio import events
import os
from deepcom.apps import DeepcomConfig
from deepviewcore.Video import Video
import threading
from deepcom.models import VideoModel
from deepcom.services.ParametersService import ParametersService
from deepcom.services.utils import get_particles_by_second, segment
from django.utils import timezone

class VideoService:
    processes = {}
    lock = threading.Lock()

    def __init__(self):
        pass

    def video_exists_in_DB(videoPath=None, videoName=None):
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

    def validate_video_file(filename: str):
        videos_path = DeepcomConfig.videos_path
        return os.path.isfile(os.path.join(videos_path, filename)) and \
            filename.lower().endswith(DeepcomConfig.allowed_extensions)

    def get_available_videos_in_folder():
        """Gets available data from videos. It will search for videos in 
        the videos folder and also for processed data in the database.

        For that data in the database without a corresponding video file, 
        some features will be disabled: 
          - Frame processor
          - Video player
          - Event list

        For those videos present in the videos folder, dictionaries with the 
        data will be used. Each video stats is a dictionary with the following keys:
         - name: video name
         - size_in_MB: video size in MB
         - duration_in_seconds: video duration in seconds
         - fps: video frames per second
         - status: video status. (processing, processed, stopped, unprocessed)
        """

        videos_names = []

        # Videos from the videos folder
        for filename in os.listdir(DeepcomConfig.videos_path):
            if VideoService.validate_video_file(filename):
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

    def get_all_available_video_data():
        videos_in_folder = VideoService.get_available_videos_in_folder()
        videos_in_db = VideoModel.objects.all()

        videos_in_db_only = [
            video for video in videos_in_db if not os.path.basename(video.video_path) in [video['name'] for video in videos_in_folder]
        ]

        videos_in_db_response = [
            {
                'name': os.path.basename(video.video_path),
                'status': video.status,
                'fps': video.frame_rate,
                'video_missing': True,
            }

            for video in videos_in_db_only
        ]

        return videos_in_folder + videos_in_db_response



    def stopProcessing(videoPath):
        if videoPath in VideoService.processes:
            with VideoService.lock:
                video: Video = VideoService.processes[videoPath]
                video.stop_processing()
                return True
        else:
            return False

    def processVideo(video_path):
        """Processes a video and returns the processed video stats.
        """
        if VideoService.video_exists_in_DB(video_path):
            print(f"Video processed exists in database. Removing {video_path}...")
            VideoModel.objects.filter(video_path=video_path).delete()
        else:
            print(f"Video processed does not exist. Adding {video_path}...")
      
        core_video = Video(video_path)
        video_stats = core_video.getStats()

        # Create a new video model
        model_video = VideoModel(
          video_path=video_path, 
          by_second=[], 
          seconds_with_events=[],
          events=[],
          frame_rate=core_video.getFrameRate())
          
        model_video.save()

        def getParticleData(object):
            return {
                'x': object['circle'][0][0],
                'y': object['circle'][0][1],
                'radius': object['circle'][1],
                'area': object['area'],
            }

        

        # Get processing parameters
        options = ParametersService.getParametersForVideo(video_path)

        def formatEvent(event):
            return {
                'frame_index': event['frame_index'],
                'x': event['circle'][0][0],
                'y': event['circle'][0][1],
                'radius': event['circle'][1],
                'area': event['area'],
            }
        
        def saveData(results):
            frames, events = results
            formatted_frames = [] 
            for cur_frame in frames:
                frame = {
                    'particles': [getParticleData(object) for object in cur_frame],
                }
                formatted_frames.append(frame)

            by_second = [{"mode": mode}
                          for mode in get_particles_by_second(formatted_frames, int(core_video.getFrameRate()))]

            model_video.by_second.extend(by_second)
            model_video.events.extend([formatEvent(event) for event in events])            
            model_video.save()

        def process():
            model_video.status = 'processing'
            model_video.save()

            # Save each 2010 frames (67 seconds of video)
            core_video.frame_interval = 2010
            core_video.process(
                action=saveData, 
                showContours=False, 
                options=options)
            del VideoService.processes[video_path]

            ret, _ = core_video.cap.read()
            if not ret and core_video.keep_processing:
                model_video.status = 'processed'
            else:
                model_video.status = 'stopped'
                core_video.setFrameIndex(
                    core_video.getCurrentFrameIndex() - 1)

            now = timezone.now()
                 
            model_video.spent_time = (now - model_video.created_at).total_seconds()

            
            model_video.save()
            print(
                f"THREAD FINISHED VideoService.processes--> {VideoService.processes.__str__()}")

        VideoService.processes[video_path] = core_video
        new_thread = threading.Thread(target=process)
        new_thread.start()

    def processFrame(videoPath, frameIndex, params):
        video = Video(videoPath)
        video.setFrameIndex(frameIndex)
        return video.processFrame(options=params)

    def getParticlesBySecond(videoPath: str):
        if not VideoService.video_exists_in_DB(videoPath):
            raise Exception(f"Couldn't get particles by second because <{videoPath}> video doesn't exist")

        model: VideoModel = VideoService.getVideoModel(videoPath)
        by_second = [second['mode'] for second in model.by_second]
        return by_second

    def getEvents(videoPath: str):
        if not VideoService.video_exists_in_DB(videoPath):
            raise Exception(f"Couldn't get events because video <{videoPath}> doesn't exist")

        model: VideoModel = VideoService.getVideoModel(videoPath)
        events = model.events
        return events
        
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