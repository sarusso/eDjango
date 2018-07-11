#  Serve static if not debug mode

import os
from django.conf.urls import patterns, url
from edjango import settings
from edjango.common.utils import discover_apps


# Setup logging
import logging
logger = logging.getLogger(__name__)

# Get admin files location
import django
admin_files_path = '/'.join(django.__file__.split('/')[0:-1]) + '/contrib/admin/static/admin'

urlpatterns = patterns('')

if not settings.DEBUG:
    urlpatterns += patterns('',
    # Admin
    (r'^static/admin/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': admin_files_path} ),
    )

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
            logger.info('Serving static for app "{}" from document root "{}"'.format(app, document_root))
            urlpatterns += patterns('',
            # Static
            (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': document_root} ),
            )
        else:
            logger.warning('No static files?!')








