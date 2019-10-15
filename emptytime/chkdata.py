import os
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emptytime.settings")
import django
django.setup()
# HTTP GET Request
from timetable.models import User


now = time.time()
for i in User.objects.all():
    if (now - float(i.token_text)) > 900:
        i.delete()