# -*- coding: UTF-8 -*-
# Copyright 2016-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Extends :mod:`lino_xl.lib.working` for Lino Noi.

See :doc:`/specs/noi/working`.

"""

from lino_xl.lib.working import *


class Plugin(Plugin):

    ticket_model = 'tickets.Ticket'

    needs_plugins = ['lino_noi.lib.tickets']

    # def setup_reports_menu(self, site, user_type, m):
    def setup_main_menu(self, site, user_type, m):
        super(Plugin, self).setup_main_menu(site, user_type, m)
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('working.ServiceReports')
        # m.add_action('working.MySessions', action='print_activity_report')


    def get_dashboard_items(self, user):
        super(Plugin, self).get_dashboard_items(user)
        if user.authenticated:
            yield self.site.models.working.WorkedHours
