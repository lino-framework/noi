# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds voting functionality.

.. autosummary::
   :toctree:

    choicelists
    models
    mixins
    fixtures.demo2

"""

from lino.api import ad, _

from lino.core.utils import resolve_model

class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    verbose_name = _("Votes")

    ## settings
    votable_model = 'tickets.Ticket'
    """The things we are voting about. A string referring to the model
    which represents a votable in your application.  Default value is
    ``'tickets.Ticket'`` (referring to
    :class:`lino_noi.lib.tickets.models.Ticket`).

    """

    def on_site_startup(self, site):
        self.votable_model = resolve_model(self.votable_model)
        super(Plugin, self).on_site_startup(site)
        
    def setup_main_menu(config, site, profile, m):
        mg = site.plugins.office
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('votes.MyOffers')
        m.add_action('votes.MyTasks')

    def setup_explorer_menu(config, site, profile, m):
        p = site.plugins.tickets
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('votes.AllVotes')
        m.add_action('votes.VoteStates')


    def get_dashboard_items(self, user):
        if user.authenticated:
            yield self.site.actors.votes.MyOffers
            yield self.site.actors.votes.MyTasks
