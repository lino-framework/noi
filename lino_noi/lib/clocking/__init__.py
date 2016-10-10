# Copyright 2008-2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Adds functionality for managing worktime clocking.

.. autosummary::
   :toctree:

    models
    actions
    roles
    ui

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    verbose_name = _("Clocking")

    needs_plugins = ['lino_noi.lib.noi']

    ticket_model = 'contacts.Partner'

    def on_site_startup(self, site):
        from lino.core.utils import resolve_model
        self.ticket_model = resolve_model(self.ticket_model)

    def setup_main_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('clocking.MySessions')
        # m.add_action('clocking.MySessionsByDate')
        # m.add_action('clocking.WorkedHours')

    def setup_config_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('clocking.SessionTypes')

    def setup_explorer_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('clocking.Sessions')
