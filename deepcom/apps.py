from django.apps import AppConfig
from os import path

from DeepView.settings import STATIC_URL

class DeepcomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'deepcom'
    videos_path = STATIC_URL + 'videos/'
    allowed_extensions = ('.mp4')

    def getVideoPath(video_name: str) -> str:
      return path.join(DeepcomConfig.videos_path, video_name)
