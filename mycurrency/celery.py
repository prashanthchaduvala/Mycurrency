from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycurrency.settings')
app = Celery('mycurrency')
 
app.config_from_object('django.conf:settings', namespace='CELERY')
 
# CELERY_BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672//'

app.autodiscover_tasks()

# celery -A mycurrency worker -l info
# celery -A mycurrency beat -l info  
