import os, sys
import django.core.handlers.wsgi
os.environ['PYTHON_EGG_CACHE'] = '/home/ford/local/lib/python2.6/site-packages'
os.environ['DJANGO_SETTINGS_MODULE'] = 'ftrain.settings'

#Calculate the path based on the location of the WSGI script.
apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)

application = django.core.handlers.wsgi.WSGIHandler()
