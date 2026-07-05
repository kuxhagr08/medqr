"""
WSGI config for medical_qr project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_qr.settings')

application = get_wsgi_application()

# Run migrations if on serverless (db in /tmp is ephemeral on every cold start)
from django.conf import settings as dj_settings
import sqlite3, pathlib
db_name = dj_settings.DATABASES['default'].get('NAME', '')
if str(db_name).startswith('/tmp'):
    call_command('migrate', interactive=False)
