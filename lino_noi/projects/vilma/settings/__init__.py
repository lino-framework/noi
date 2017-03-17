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
    title = u"Külaministeerium"
    

