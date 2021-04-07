# Copyright 2017 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Lino Noi extension of :mod:`lino_xl.lib.cal`.

"""

from lino_xl.lib.cal import Plugin


class Plugin(Plugin):

    extends_models = ['Event']
    needs_plugins = ['lino_noi.lib.noi']
