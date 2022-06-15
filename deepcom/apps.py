from django.apps import AppConfig
from os import path

class DeepcomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'deepcom'
    videos_path = 'C:/Users/migue/Documents/U/4to/TFG/Videos'
    allowed_extensions = ('.mp4')

    def getVideoPath(video_name: str) -> str:
      return path.join(DeepcomConfig.videos_path, video_name)
