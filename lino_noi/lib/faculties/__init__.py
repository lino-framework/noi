# -*- coding: UTF-8 -*-
# Copyright 2011-2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""Adds the notions of "competences" and "faculties" to your ticket
management.

.. autosummary::
   :toctree:

   models

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    verbose_name = _("Faculties")

    needs_plugins = ['lino_noi.lib.noi']

    # def setup_main_menu(self, site, profile, m):
    #     mg = self.get_menu_group()
    #     m = m.add_menu(mg.app_label, mg.verbose_name)
    #     m.add_action('tickets.UnassignedTickets')
        # m = m.add_menu(self.app_label, self.verbose_name)
        # m.add_action('faculties.Faculties')
        # m.add_action('faculties.Competences')

    def setup_config_menu(self, site, profile, m):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('faculties.TopLevelFaculties')
        m.add_action('faculties.AllFaculties')
        m.add_action('faculties.FacultyTypes')

    def setup_explorer_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('faculties.Competences')
