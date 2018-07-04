
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

#=================
#  Send email
#=================

EDJANGO_EMAIL_FROM = os.environ.get('EDJANGO_EMAIL_FROM', 'info@edjango.project')
EDJANGO_EMAIL_APIKEY = os.environ.get('EDJANGO_EMAIL_APIKEY', None)

def send_email(to, subject, text):

    import sendgrid
    from sendgrid.helpers.mail import *

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
    





















