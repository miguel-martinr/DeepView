from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.say_hello),
    path('processed-video/', views.processed_video),
    path('available-videos/', views.available_videos),
]


