# import os ; print "20161219 %s (pid:%s)" % (__name__, os.getpid())

import datetime

from ..settings import *


class Site(Site):
    # default_ui = 'lino_extjs6.extjs6'
    the_demo_date = datetime.date(2017, 3, 16)
    languages = "en et"

SITE = Site(globals())
# print "20161219 b"
DEBUG = True

# the following line should not be active in a checked-in version
# DATABASES['default']['NAME'] = ':memory:'
