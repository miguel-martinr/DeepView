from django.http import HttpRequest
import numpy as np
from deepcom.apps import DeepcomConfig
from deepcom.models import VideoModel
from scipy import stats


def segment(values, size):
    segments = []
    for i in range(0, len(values), size):
        segments.append(values[i:i+size])
    return segments


def mode_by_segment(segments):
    result = []
    for segment in segments:                
        mode = stats.mode(segment)[0]
        result.append(int(mode[0]))
    return result



def get_particles_quantity(frames: list, unit='seconds'):
    groupSizes = {
        'seconds': 30,
        'minutes': 60,
        'hours': 60 * 60,
    }

    particles_per_frame = [len(frame['particles']) for frame in frames]

    seconds_segments = segment(particles_per_frame, 30)
    by_second = mode_by_segment(seconds_segments)

    if unit == 'seconds': return by_second

    if unit == 'minutes': 
      
      minutes_segments = segment(by_second, 60)
      by_minute = mode_by_segment([np.sum(min) for min in minutes_segments])
      return by_minute
    
    else:
      hours_segments = segment(by_second, 1800)
      by_hour = mode_by_segment([np.sum(hour) for hour in hours_segments])
      return by_hour



def get_data(request: HttpRequest):
    """
    Get data from the video.
    """

    try:
        video_name = request.GET.get('video_name')
    except KeyError:
        return {
            'success': False,
            'message': 'No video name provided',
        }

    dataGetters = {
        'ParticlesAverage': get_particles_quantity,
    }

    try:
        type = request.GET.get('type')
    except KeyError:
        type = 'ParticlesAverage'

    try:
        unit = request.GET.get('unit')
    except KeyError:
        unit = 'minutes'

    response = {
        'success': True,
    }

    video_path = DeepcomConfig.getVideoPath(video_name)
    if len(VideoModel.objects.filter(video_path=video_path)) == 0:
        return {
            'success': False,
            'message': 'Video not found',
        }

    video_model: VideoModel = VideoModel.objects.get(video_path=video_path)
    data = dataGetters[type](video_model.frames, unit)

    response["data"] = data
    return response
