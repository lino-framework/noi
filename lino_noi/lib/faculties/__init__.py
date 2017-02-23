# -*- coding: UTF-8 -*-
# Copyright 2011-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Adds the notions of "competences" and "faculties" to your ticket
management.

.. autosummary::
   :toctree:

   models
   ui
   roles

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    """.. attribute:: demander_model

        The model of objects to be used as :attr:`demander
        <lino_noi.lib.faculties.models.Demand.demander>` of skill
        demands. The default value is :class:`Ticket
        <lino_noi.lib.tickets.models.Ticket>`.

    .. attribute:: supplier_model

        The model of objects to be used as :attr:`supplier
        <lino_noi.lib.faculties.models.Competence.supplier>` of skill
        offers. The tefault value is  :class:`Person
        <lino_noi.lib.tickets.models.Ticket>`.

    """

    verbose_name = _("Skills")

    needs_plugins = [
        'lino_noi.lib.noi', 'lino_noi.lib.tickets',
        'lino_noi.lib.contacts']

    demander_model = 'tickets.Ticket'
    supplier_model = 'contacts.Person'

    def on_site_startup(self, site):
        self.demander_model = site.models.resolve(self.demander_model)
        self.supplier_model = site.models.resolve(self.supplier_model)
        super(Plugin, self).on_site_startup(site)
        
    def setup_main_menu(self, site, profile, m):
        # mg = self.get_menu_group()
        mg = site.plugins.tickets
        m = m.add_menu(mg.app_label, mg.verbose_name)
        # m.add_action('faculties.Faculties')
        # m.add_action('faculties.Competences')
        m.add_action('faculties.MyOffers')

    def setup_config_menu(self, site, profile, m):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('faculties.TopLevelSkills')
        m.add_action('faculties.AllSkills')
        m.add_action('faculties.SkillTypes')

    def setup_explorer_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        # m.add_action('faculties.Competences')
        m.add_action('faculties.Offers')
        m.add_action('faculties.Demands')
