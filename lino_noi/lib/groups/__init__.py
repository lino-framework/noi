# Copyright 2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Lino Noi extension of :mod:`lino_xl.lib.groups`.

"""

from lino_xl.lib.groups import Plugin
from lino.api.ad import _

class Plugin(Plugin):

    extends_models = ['Group']
    verbose_name = _("Teams")
