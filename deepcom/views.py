


from django.http import HttpResponse
from django.shortcuts import render


from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from deepcom.controllers.processed_video.get import get_processed_video_controller

from deepcom.models import ParticleData, ProcessedVideo
from .serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


def processed_video(request):
  if request.method == 'GET':
    return get_processed_video_controller(request)
  else:
    return HttpResponse(status=404)

    


def say_hello(request):

    return render(request, 'hello.html', {
        'name': 'Miguel',
    })
