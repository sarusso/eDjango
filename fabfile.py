from fabric.api import local, task
from edjango.common.utils import booleanize
from edjango.common.utils import discover_apps
import os


# Try to understand where we are
if not os.path.isfile('manage.py'):
    if os.path.isfile('../../manage.py'):
        os.chdir('../../')
    else:
        abort('Sorry, could not find fabfile. Are you in the root directory or in an app directory?')

#--------------------
# Utility functions
#--------------------

def run(command):
    local(command)
        

#--------------------
# Run
#--------------------

@task
def shell():
    run('python manage.py shell')


@task
def runserver(noreload=False):
    if isinstance(noreload,str) and noreload.upper()=='FALSE':
        noreload=False
    if noreload:
        run('python manage.py runserver 0.0.0.0:8080 --noreload')
    else:
        run('python manage.py runserver 0.0.0.0:8080')


#-----------------------------
#   Install
#-----------------------------

@task
def install(what=None, env="local", noinput=False):
    run("python manage.py makemigrations")
    if noinput:
        run("python manage.py migrate --noinput")
    else:
        run("python manage.py migrate")


#-----------------------------
#   Populate
#-----------------------------

@task
def populate(env="local"):
    
    for app in discover_apps('edjango', only_names=True):
        
        # Check if we have the populate:
        populate_file = 'edjango/{}/management/commands/{}_populate.py'.format(app,app)
        if os.path.isfile(populate_file):
            print 'Poulate found for {} and executing...'.format(app)
            run("python manage.py {}_populate".format(app))
        else:
            print 'No poulate found for {}... ({})'.format(app,populate_file)


#-----------------------------
#   Migrations
#-----------------------------
@task
def makemigrations(what=None, env="local"):
    run("python manage.py makemigrations")


@task
def migrate(app=None):
    if app:
        run('python manage.py migrate {}'.format(app))
    else:
        run('python manage.py migrate')        


#-----------------------------
#   Tests
#-----------------------------
@task
def test():
    run("python manage.py test")


#-----------------------------
#   Deploy
#-----------------------------
@task
def collect():
    run('python manage.py collectstatic')








