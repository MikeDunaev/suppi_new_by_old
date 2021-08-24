# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u1391713/data/www/suppi.ru/analytics')
sys.path.insert(1, '/var/www/u1391713/data/suppivenv/lib/python3.9/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'analytics.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
