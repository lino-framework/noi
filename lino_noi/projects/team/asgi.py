import os
from channels.asgi import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lino_noi.projects.team.settings.demo")

channel_layer = get_channel_layer()
