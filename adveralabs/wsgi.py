"""
WSGI config for adveralabs project.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adveralabs.settings')

application = get_wsgi_application()

