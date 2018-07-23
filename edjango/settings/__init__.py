
# Import common settings
from edjango.settings.common import *

# Apps setttings auto discovery

from edjango.common.utils import discover_apps


for app in discover_apps('edjango', only_names=True):

    # Check if we have the populate:
    settings_file = 'edjango/{}/settings.py'.format(app)
    if os.path.isfile(settings_file):
        
        app_settings_module = 'edjango.{}.settings'.format(app)

        # A bit triky but should be fine...
        exec('from {} import *'.format(app_settings_module))
