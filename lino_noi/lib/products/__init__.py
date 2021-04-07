# -*- coding: UTF-8 -*-
# Copyright 2014-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
An extension of :mod:`lino_xl.lib.products`
"""

from lino_xl.lib.products import Plugin

class Plugin(Plugin):

    price_selector = "working.SessionType"
