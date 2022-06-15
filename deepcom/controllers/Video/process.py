from os import path
import json
from django.http import HttpRequest, HttpResponse
from deepcom.apps import DeepcomConfig
from deepcom.models import VideoModel

from deepcom.services.videos import VideoService


def process_video(video_name):
    video_path = DeepcomConfig.getVideoPath(video_name)

    VideoService.processVideo(video_path)
    response = {
      'success': True,
      'message': 'Video is being processed'
    }

    return response