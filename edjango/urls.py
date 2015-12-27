"""edjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

# Apps urls auto-discovery
from edjango.common.utils import discover_apps
import os

for app in discover_apps('edjango', only_names=True):
        
    # Check if we have the urls:
    urls_file = 'edjango/{}/urls.py'.format(app,app)
    if os.path.isfile(urls_file):

        urlpatterns.append(url(r'^', include('edjango.{}.urls'.format(app))))

























