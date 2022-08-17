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

    default_top_hat_parameters = {
      "kernelWidth": 9,
      "kernelHeight": 9
    }

    default_threshold_parameters = {
      'thresh': 20
    }

    default_preprocess_parameters = {
      "top_hat": default_top_hat_parameters
    }

    default_process_parameters = {
      "threshold": default_threshold_parameters,
    }

    default_events_parameters = {
      "minArea": 200,
    }

    default_processing_parameters = {
      "preprocess": default_preprocess_parameters,
      "process": default_process_parameters,
      "events": default_events_parameters
    }
