# -*- coding: UTF-8 -*-
# Copyright 2016-2017 Luc Saffre
# License: BSD (see file COPYING for details)

from lino_xl.lib.tickets.models import *
from lino.api import _

Ticket.hide_elements('closed')


# class Ticket(Ticket):
#     class Meta(Ticket.Meta):
#         app_label = 'tickets'
#         verbose_name = _("Plea")
#         verbose_name_plural = _("Pleas")
#         abstract = dd.is_abstract_model(__name__, 'Ticket')

# ActiveTickets._label = _("Active pleas")
# UnassignedTickets._label = _("Unassigned pleas")
# PublicTickets._label = _("Public pleas")
# TicketsToTriage._label = _("Pleas to triage")
# TicketsToTalk._label = _("Pleas to talk")
# # TicketsToDo._label = _("Pleas to to")
# TicketsFixed._label = _("Fixed pleas")
# TicketsReported._label = _("Introduced pleas")
# TicketsByReporter._label = _("Introduced pleas")
# AllTickets._label = _("All pleas")

dd.update_field(
    'tickets.Ticket', 'upgrade_notes', verbose_name=_("Solution"))

# dd.update_field(
#     'tickets.Ticket', 'state', default=TicketStates.todo.as_callable)

class TicketDetail(TicketDetail):
    main = "general history_tab more"

    general = dd.Panel("""
    general1:60 votes.VotesByVotable:20 uploads.UploadsByController
    description:30 comments.CommentsByRFC:30 faculties.DemandsByDemander #clocking.SessionsByTicket:20
    """, label=_("General"))

    general1 = """
    summary:40 id:6 deadline
    user:12 end_user:12 #faculty #topic
    site workflow_buttons
    """

    history_tab = dd.Panel("""
    changes.ChangesByMaster:50 #stars.StarsByController:20
    """, label=_("History"), required_roles=dd.login_required(Triager))

    more = dd.Panel("""
    more1:60 #faculties.AssignableWorkersByTicket:20
    upgrade_notes LinksByTicket faculties.OffersByDemander
    """, label=_("More"), required_roles=dd.login_required(Triager))

    more1 = """
    created modified ticket_type:10
    state priority project
    # standby feedback closed
    """



Tickets.detail_layout = TicketDetail()
