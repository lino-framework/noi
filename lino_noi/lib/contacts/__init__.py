# Copyright 2015-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""
Lino Noi extension of :mod:`lino_xl.lib.contacts`.

.. autosummary::
   :toctree:

    models

"""

from lino_xl.lib.contacts import Plugin


class Plugin(Plugin):
    
    extends_models = ['Person']

