
import os


# From DockerOps
def booleanize(*args, **kwargs):
    # Handle both single value and kwargs to get arg name
    name = None
    if args and not kwargs:
        value=args[0]
    elif kwargs and not args:
        for item in kwargs:
            name  = item
            value = kwargs[item]
            break
    else:
        raise Exception('Internal Error')
    
    # Handle shortcut: an arg with its name equal to ist value is considered as True
    if name==value:
        return True
    
    if isinstance(value, bool):
        return value
    else:
        if value.upper() in ('TRUE', 'YES', 'Y', '1'):
            return True
        else:
            return False
            
            
def discover_apps(folder, only_names=False):

    # List directories in folder
    dirs = [ dir for dir in os.listdir(folder) if os.path.isdir(os.path.join(folder,dir)) ]
    
    apps = ()
    # Detect apps
    for dir in dirs:
        if dir.endswith('app'):
            if only_names:
                apps = apps + (dir,)
            else:    
                apps = apps + ('edjango.{}'.format(dir),)
        
    
    return apps



























