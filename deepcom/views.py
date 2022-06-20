import mimetypes
import os
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from ranged_response import RangedFileResponse
from deepcom.apps import DeepcomConfig





# Hello
def say_hello(request):
    return render(request, 'hello.html', {
        'name': 'Miguel',
    })


def video_stream(request, video_name):
    file = DeepcomConfig.getVideoPath(video_name)
    if not os.path.isfile(file):
        return HttpResponseNotFound()
    response = RangedFileResponse(
        request, open(file, 'rb'),
        content_type=mimetypes.guess_type(file)[0]
    )
    response['Content-Length'] = os.path.getsize(file)
    return response





    


