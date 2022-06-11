
from this import s
from django.http import HttpResponse
from django.shortcuts import render
from bson.json_util import dumps

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions

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
    # data = [
    #   {"cirlce": [(0.0, 0.0), 3.2], "area": 5.0},
    #   {"cirlce": [(0.0, 0.0), 3.2], "area": 5.0},
    # ]

    data = ProcessedVideo.objects.mongo_find()
    return HttpResponse(dumps(data), content_type='application/json')


def say_hello(request):

    return render(request, 'hello.html', {
        'name': 'Miguel',
    })
