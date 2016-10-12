# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
from __future__ import unicode_literals
from __future__ import print_function

from lino.api import rt, dd


def objects():
    SessionType = rt.modules.clocking.SessionType
    yield SessionType(id=1, name="Default")

