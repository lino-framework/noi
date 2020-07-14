# -*- coding: UTF-8 -*-
# Copyright 2014-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""This is the main module of Lino Noi.

.. autosummary::
   :toctree:

   lib


"""

from lino_noi.setup_info import SETUP_INFO

__version__ = SETUP_INFO['version']

srcref_url = 'https://github.com/lino-framework/noi/blob/master/%s'
intersphinx_urls = dict(docs="http://noi.lino-framework.org")
doc_trees = ['docs']
