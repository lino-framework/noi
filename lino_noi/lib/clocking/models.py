# -*- coding: UTF-8 -*-
# Copyright 2016-2017 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

from lino_xl.lib.clocking.models import *
from lino.api import _
from lino.mixins.periods import DateRange
from lino_xl.lib.excerpts.mixins import Certifiable
from lino_xl.lib.contacts.mixins import ContactRelated
from lino_xl.lib.tickets.choicelists import TicketStates
# from .actions import StartTicketSessionViaVote, EndTicketSessionViaVote, StartTicketSessionViaSession, StartTicketSessionViaWish

# #Moved to XL
# dd.inject_field(
#     "users.User", 'open_session_on_new_ticket',
#     models.BooleanField(_("Open session on new ticket"), default=False))

# if dd.is_installed('votes'):
#     dd.inject_action(
#         "votes.Vote",
#         start_session=StartTicketSessionViaVote())
#     dd.inject_action(
#         "votes.Vote",
#         end_session=EndTicketSessionViaVote())

# dd.inject_action(
#         "clocking.Session",
#         start_session=StartTicketSessionViaSession()
#         )
# dd.inject_action(
#         "deploy.Deployment",
#         start_session=StartTicketSessionViaWish()
#         )


@dd.python_2_unicode_compatible
class ServiceReport(UserAuthored, ContactRelated, Certifiable, DateRange):
    class Meta:
        app_label = 'clocking'
        verbose_name = _("Service Report")
        verbose_name_plural = _("Service Reports")

    interesting_for = dd.ForeignKey(
        'contacts.Partner',
        verbose_name=_("Interesting for"),
        blank=True, null=True,
        help_text=_("Only tickets interesting for this partner."))

    ticket_state = TicketStates.field(
        null=True, blank=True,
        help_text=_("Only tickets in this state."))

    def __str__(self):
        return "{} {}".format(self._meta.verbose_name, self.pk)

    def get_tickets_parameters(self, **pv):
        """Return a dict with parameter values for `tickets.Tickets` based on
        the options of this report.

        """
        pv.update(start_date=self.start_date, end_date=self.end_date)
        pv.update(interesting_for=self.interesting_for)
        if self.ticket_state:
            pv.update(state=self.ticket_state)
        return pv
        

from .ui import *

    
