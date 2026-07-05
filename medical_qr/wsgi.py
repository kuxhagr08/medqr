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

# If running on Vercel serverless, run migrations on boot since /tmp is ephemeral
if '/var/task' in str(__file__) or os.environ.get('VERCEL') == '1' or os.environ.get('AWS_EXECUTION_ENV') is not None:
    call_command('migrate', interactive=False)
