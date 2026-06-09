"""
WSGI config for joke_generator project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'joke_generator.settings')

application = get_wsgi_application()
