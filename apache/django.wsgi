import os
import site
import sys

site.addsitedir('/opt/venv/lib/python2.6/site-packages')
sys.path.append('/opt/starandshadow/')
sys.path.append('/opt/starandshadow/ss/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ss.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
