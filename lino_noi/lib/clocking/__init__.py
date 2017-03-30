# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""Clocking specific for the Team variant of Lino Noi.

See :ref:`noi.specs.clocking`.

.. autosummary::
   :toctree:

   models
   fixtures


"""

from lino_xl.lib.clocking import *


class Plugin(Plugin):

    ticket_model = 'tickets.Ticket'

    needs_plugins = ['lino_noi.lib.tickets']

    def setup_reports_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('clocking.ServiceReports')
        # m.add_action('clocking.MySessions', action='print_activity_report')
