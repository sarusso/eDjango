from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User
from django.conf import settings

class Command(NoArgsCommand):

    def handle_noargs(self, *args, **kwargs):
 
        if not User.objects.filter(username='admin').exists():
            print 'Creating default admin: user=admin, pass=admin. Change it!!'
            admin = User.objects.create_superuser('admin', 'admin@edjango.local', 'admin')
            admin.save()


