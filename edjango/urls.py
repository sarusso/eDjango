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

import os
from django.conf.urls import include, url
from django.contrib import admin
from edjango import settings
from edjango.common.utils import discover_apps

# Setup logging
import logging
logger = logging.getLogger(__name__)


#============================
#  Initialize
#============================

# Initialize urlpatterns including the admin view
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

# Discover apps
apps =  discover_apps('edjango', only_names=True)


#============================
#  Add views for apps
#============================

for app in apps:
        
    # Check if we have the urls:
    urls_file = 'edjango/{}/urls.py'.format(app,app)
    if os.path.isfile(urls_file):

        urlpatterns.append(url(r'^', include('edjango.{}.urls'.format(app))))


#============================
#  Serve static if required
#============================

# Get admin files location
import django
admin_files_path = '/'.join(django.__file__.split('/')[0:-1]) + '/contrib/admin/static/admin'
 
if not settings.DEBUG:
    # Admin
    urlpatterns.append(url(r'^static/admin/(?P<path>.*)$', django.views.static.serve, {'document_root': admin_files_path} ))
 
    # Apps  auto discovery for static files
    apps = list(discover_apps('edjango', only_names=True))
     
    # Remove base app
    apps.remove('base_app')
     
    if len(apps) > 1:
        logger.error('Cannot serve static file sfor app as more than one app found ({}). Use collect_static.'.format(apps))
     
    else:
         
        app=apps[0]
        document_root = 'edjango/{}/static'.format(app)
         
        if os.path.isdir(document_root):
            logger.info('Serving static files for app "{}" from document root "{}"'.format(app, document_root))
            # Static
            urlpatterns.append(url(r'^static/(?P<path>.*)$', django.views.static.serve, {'document_root': document_root} ))
        else:
            logger.warning('Not static files to serve?!')
else:
    logger.info('Not serving static files at all as DEBUG=True (Django will do it automatically)')























