from os import path
import json
from django.http import HttpRequest, HttpResponse
from deepcom.apps import DeepcomConfig
from deepcom.models import VideoModel

from deepcom.services.videos import VideoService


def process_video_controller(request: HttpRequest):
    decoded_body = request.body.decode('utf-8')
    # print(f"#############BODY: {decoded_body}###################")
    json_body = json.loads(decoded_body)
    video_path = path.join(DeepcomConfig.videos_path, json_body['video_name'])

    VideoService.processVideo(video_path)
    response = {
      'success': True,
      'message': 'Video is being processed'
    }

    return HttpResponse(json.dumps(response), status=200, content_type='application/json')