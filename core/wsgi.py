import os
import socketio
from moderators.views import sio
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
application = socketio.WSGIApp(sio, application)