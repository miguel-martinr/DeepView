import os

from deepcom.apps import DeepcomConfig
from deepviewcore.Video import Video


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
            current_stats['status'] = 'UNPROCESSED'
            videos_stats.append(current_stats)
        return videos_stats
