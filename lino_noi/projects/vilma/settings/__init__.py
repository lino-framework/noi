# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""The :xfile:`settings.py` modules for this variant.

.. autosummary::
   :toctree:

   demo

"""


from lino_noi.projects.team.settings import *


class Site(Site):
    languages = 'et'
    title = u"Külavalitsus"
    

    def setup_plugins(self):
        super(Site, self).setup_plugins()
        self.plugins.tickets.configure(
            site_model='cal.Room')
