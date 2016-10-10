# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""Fixtures specific for Lino Care.

.. autosummary::
   :toctree:

   models
   fixtures.demo


"""

from lino_noi.lib.tickets import *
from lino.api import _


class Plugin(Plugin):
    verbose_name = _("Pleas")
    extends_models = ['Ticket']
    
