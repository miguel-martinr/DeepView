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
        result.append(sum([len(frame['particles']) for frame in segment]) / len(segment))

    return result


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

    try:
        params = request.GET.get('params')
    except KeyError:
        return {
            'success': False,
            'message': 'No params provided',
        }

    params = json.loads(params)

    # Summarize frames
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

    summarizeFrames = params.get('summarizeFrames')
    if summarizeFrames:
        response['message'] = {
            'frames': summarize_frames(summarizeFrames, video_model.frames),
        }
    else:
        response["message"] = {
            "frames": video_model.frames
        }

    return response
