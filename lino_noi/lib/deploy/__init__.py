# Copyright 2008-2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Adds functionality for managing "milestones" and "deployments".

.. autosummary::
   :toctree:

    models
    desktop

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    verbose_name = _("Deploy")

    needs_plugins = ['lino_noi.lib.tickets']

    # def setup_main_menu(self, site, profile, m):
    #     p = self.get_menu_group()
    #     m = m.add_menu(p.app_label, p.verbose_name)
    #     # m.add_action('tickets.Tickets')

    # def setup_config_menu(self, site, profile, m):
    #     p = self.get_menu_group()
    #     m = m.add_menu(p.app_label, p.verbose_name)
    #     # m.add_action('tickets.Projects')

    def setup_explorer_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('deploy.Milestones')
        m.add_action('deploy.Deployments')
