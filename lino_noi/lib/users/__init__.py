# Copyright 2015-2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Lino Noi extension of :mod:`lino.modlib.users`.

.. autosummary::
   :toctree:

    models
    fixtures.demo
    fixtures.demo2

"""

from lino.modlib.users import Plugin


class Plugin(Plugin):
    needs_plugins = ['lino_xl.lib.countries']
    
    extends_models = ['User']

