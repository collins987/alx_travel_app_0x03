# alx_travel_app/celery.py
import os
from celery import Celery

# set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')

app = Celery('alx_travel_app')

# load config from Django settings, using CELERY_ namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# auto-discover tasks from installed apps
app.autodiscover_tasks()
