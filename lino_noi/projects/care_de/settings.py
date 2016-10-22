"""The :xfile:`settings.py` file for this project.
"""

from atelier.utils import i2d
from lino_noi.projects.care.settings import *


class Site(Site):
    the_demo_date = i2d(20150523)
    languages = "de fr en"


SITE = Site(globals())
DEBUG = True

# the following line should not be active in a checked-in version
# DATABASES['default']['NAME'] = ':memory:'
