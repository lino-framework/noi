# -*- coding: UTF-8 -*-
# Copyright 2016-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models specific for the Team variant of Lino Noi.

Defines a customized :class:`TicketDetail`.

"""

from lino_xl.lib.tickets.models import *
from lino.modlib.users.mixins import Assignable
from lino.api import _


class Ticket(Ticket, Assignable):
    class Meta(Ticket.Meta):
        # app_label = 'tickets'
        abstract = dd.is_abstract_model(__name__, 'Ticket')


class TicketDetail(TicketDetail):
    """Customized detail_lyout for Tickets.  Replaces `waiting_for` by
    `faculties`

    """
    main = "general more history_tab more2 #github.CommitsByTicket"
    
    general = dd.Panel("""
    general1:60 comments.CommentsByRFC:30
    """, label=_("General"))

    general1 = """
    summary:40 id:6
    user end_user assigned_to deadline
    site topic project 
    workflow_buttons:30 private
    bottom_box
    """

    bottom_box = """
    #faculties.DemandsByDemander:20 #votes.VotesByVotable:20 
    deploy.DeploymentsByTicket:20 clocking.SessionsByTicket:20
    github.CommitsByTicket
    """

    more = dd.Panel("""
    more1 DuplicatesByTicket:20 #WishesByTicket
    description:30 upgrade_notes:20 LinksByTicket:20  
    """, label=_("More"))

    more2 = dd.Panel("""
    # deploy.DeploymentsByTicket
    faculties.DemandsByDemander
    stars.StarsByController
    uploads.UploadsByController 
    """, label=_("Even more"))

Tickets.detail_layout = TicketDetail()
Tickets.params_layout = """user end_user assigned_to not_assigned_to interesting_for site project state deployed_to
    has_project show_assigned show_active show_deployed show_todo show_private
    start_date end_date observed_event topic #feasable_by has_ref"""
MyTickets.params_layout = """
    user end_user site project state
    start_date end_date observed_event topic #feasable_by show_active"""
# Sites.detail_layout = """
# id name partner #responsible_user
# remark
# #InterestsBySite TicketsBySite deploy.MilestonesBySite
# """



