from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.say_hello),
    path(r'^processed-video/?$', views.processed_video),
]


