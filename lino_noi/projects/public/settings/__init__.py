# -*- coding: UTF-8 -*-
# Copyright 2015-2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""The :xfile:`settings.py` modules for this variant.

.. autosummary::
   :toctree:

   demo
   doctests

"""

from lino_noi.projects.team.settings.demo import *


class Site(Site):

    default_ui = 'lino_noi.lib.public'
    default_user = 'anonymous'

    # def get_installed_apps(self):
    #     yield super(Site, self).get_installed_apps()
    #     yield 'lino.modlib.bootstrap3'

