# -*- coding: UTF-8 -*-
# Copyright 2014-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""This is the main module of Lino Noi.

.. autosummary::
   :toctree:

   lib


"""

from os.path import join, dirname
fn = join(dirname(__file__), 'setup_info.py')
exec(compile(open(fn, "rb").read(), fn, 'exec'))

__version__ = SETUP_INFO['version']

srcref_url = 'https://github.com/lino-framework/noi/blob/master/%s'
# intersphinx_urls = dict(docs="http://noi.lino-framework.org")
# doc_trees = ['docs']

