
import os
import traceback
import hashlib
import random



# Setup logging
import logging
logger = logging.getLogger(__name__)

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
            

#=================
#  Send email
#=================


def send_email(to, subject, text):

    import sendgrid
    from sendgrid.helpers.mail import *
    
    # Importing here instead of on top avoids circular dependencies problems when loading booleanize in settings
    from edjango.settings import EDJANGO_EMAIL_APIKEY, EDJANGO_EMAIL_FROM

    sg = sendgrid.SendGridAPIClient(apikey=EDJANGO_EMAIL_APIKEY)
    from_email = Email(EDJANGO_EMAIL_FROM)
    to_email = Email(to)
    subject = subject
    content = Content('text/plain', text)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    #logger.debug(response.status_code)
    #logger.debug(response.body)
    #logger.debug(response.headers)
    


def format_exception(e, debug=False):
    
    # Importing here instead of on top avoids circular dependencies problems when loading booleanize in settings
    from edjango.settings import DEBUG

    if DEBUG:
        # Cutting away the last char removed the newline at the end of the stacktrace 
        return str('Got exception "{}" of type "{}" with traceback:\n{}'.format(e.__class__.__name__, type(e), traceback.format_exc()))[:-1]
    else:
        return str('Got exception "{}" of type "{}" with traceback "{}"'.format(e.__class__.__name__, type(e), traceback.format_exc().replace('\n', '|')))




# Log user activity
def log_user_activity(level, msg, request, caller=None):

    # Get the caller function name through inspect with some logic
    #import inspect
    #caller =  inspect.stack()[1][3]
    #if caller == "post":
    #    caller =  inspect.stack()[2][3]
    
    try:
        msg = str(caller) + " view - USER " + str(request.user.email) + ": " + str(msg)
    except AttributeError:
        msg = str(caller) + " view - USER UNKNOWN: " + str(msg)

    try:
        level = getattr(logging, level)
    except:
        raise
    
    logger.log(level, msg)


def username_hash(email):
    '''Create md5 base 64 (25 chrars) hash from user email:'''             
    m = hashlib.md5()
    m.update(email)
    username = m.hexdigest().decode('hex').encode('base64')[:-3]
    return username


def random_username():
    '''Create a random string of 156 chars to be used as username'''             
    username = ''.join(random.choice('abcdefghilmnopqrtuvz') for _ in range(16))
    return username


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







