from fabric.api import local, task
from edjango.common.utils import booleanize
from edjango.common.utils import discover_apps
import os

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
def runserver():
    run('python manage.py runserver 0.0.0.0:8080')


#-----------------------------
#   Install
#-----------------------------

@task
def install(what=None, env="local"):
    run("python manage.py makemigrations")
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








