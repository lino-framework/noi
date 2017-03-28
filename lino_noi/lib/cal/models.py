# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for this plugin.

"""

from lino.api import dd, _

from lino_xl.lib.cal.models import *


class EventDetail(EventDetail):
    pass    

    
Events.set_detail_layout(EventDetail())
