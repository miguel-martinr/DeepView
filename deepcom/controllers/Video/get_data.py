import json
from django.http import HttpRequest
from deepcom.apps import DeepcomConfig
from deepcom.models import VideoModel


def summarize_frames(size, frames):
    """
    Summarize frames.
    """
    result = []
    for i in range(0, len(frames), size):
        segment = frames[i:i+size]
        # print(f"###Segment: {segment}")
        result.append(sum([len(frame['particles']) for frame in segment]))

    return result


def get_particles_quantity(frames: list, unit='seconds'):
    groupSizes = {
        'seconds': 30,
        'minutes': 30 * 60,
        'hours': 30 * 60 * 60,
    }

    multiplier = groupSizes[unit]
    summarized = summarize_frames(multiplier, frames)
    return summarized


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
