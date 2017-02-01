# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Settings for providing readonly public access to the site. This
does not use :mod:`lino.modlib.extjs` but :mod:`lino.modlib.bootstrap3`.

"""

import datetime

from ..settings import *


class Site(Site):
    """Defines and instantiates a demo version of Lino Noi."""

    the_demo_date = datetime.date(2015, 5, 23)
    languages = "en de fr"
    readonly = True


team_db = DATABASES

SITE = Site(globals())

DATABASES = team_db

DEBUG = True

