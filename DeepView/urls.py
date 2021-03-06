"""DeepView URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import path, re_path


# Deepcom
from django.urls import include, path

from django.urls import include, path


def render_react(request: HttpRequest):
    return render(request, "index.html")

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('deepcom/', include('deepcom.urls')),
    re_path(r"^(?:.*)/?$", render_react),
]
