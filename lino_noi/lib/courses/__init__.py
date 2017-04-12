# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""The courses variant of Lino Noi.

.. autosummary::
   :toctree:

   models


"""

from lino_xl.lib.courses import *

class Plugin(Plugin):
    """Adds the :mod:`lino_xl.lib.votes` plugin.
    """

    extends_models = ['Course']
    def get_dashboard_items(self, user):
        for x in super(Plugin, self).get_dashboard_items(user):
            yield x
        if user.authenticated:
            yield self.site.actors.courses.MyEnrolments