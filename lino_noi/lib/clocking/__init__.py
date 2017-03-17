# Copyright 2008-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Adds functionality for managing worktime clocking.

.. autosummary::
   :toctree:

    models
    actions
    roles
    ui
    mixins

"""

import six

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    # verbose_name = _("Clocking")
    verbose_name = _("Working time")

    needs_plugins = ['lino_noi.lib.noi']

    # project_model = 'tickets.Project'
    # project_model = 'contacts.Partner'
    
    # ticket_model = 'tickets.Ticket'
    ticket_model = 'contacts.Partner'
    """The model that is to be used as the "workable".

    This must be a subclass of
    :class:`lino_noi.lib.clocking.mixins.Workable`

    """

    default_reporting_type = 'regular'

    def on_site_startup(self, site):
        from .mixins import Workable
        self.ticket_model = site.models.resolve(self.ticket_model)
        if not issubclass(self.ticket_model, Workable):
            msg = "Your plugins.clocking.ticket_model ({}) is not workable"
            msg = msg.format(self.ticket_model)
            raise Exception(msg)

        if isinstance(self.default_reporting_type, six.string_types):
            x = site.models.clocking.ReportingTypes.get_by_name(
                self.default_reporting_type)
            self.default_reporting_type = x

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

    def get_dashboard_items(self, user):
        if user.authenticated:
            yield self.site.actors.clocking.WorkedHours
        
