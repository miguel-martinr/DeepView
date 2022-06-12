from django.http import HttpResponse
from bson.json_util import dumps
from deepcom.models import VideoModel

def get_processed_video_controller(request):
  
    # data = [
    #   {"cirlce": [(0.0, 0.0), 3.2], "area": 5.0},
    #   {"cirlce": [(0.0, 0.0), 3.2], "area": 5.0},
    # ]
    data = VideoModel.objects.mongo_find()
    return HttpResponse(dumps(data), content_type='application/json')
