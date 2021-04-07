# -*- coding: UTF-8 -*-
# Copyright 2017 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
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
    # def setup_main_menu(self, site, user_type, main):
    #     super(Plugin, self).setup_main_menu(site, user_type, main)
    #     m = main.get_item(self.app_label)
    #     m.add_action('courses.MyEnrolments')
    #

    # def get_dashboard_items(self, user):
    #     for x in super(Plugin, self).get_dashboard_items(user):
    #         yield x
    #     if user.authenticated:
    #         yield self.site.models.courses.MyEnrolments
