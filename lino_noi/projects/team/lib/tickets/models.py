# -*- coding: UTF-8 -*-
# Copyright 2016-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models specific for the Team variant of Lino Noi.

Defines a customized :class:`TicketDetail`.

"""

from lino_noi.lib.tickets.models import *
from lino.api import _


class TicketDetail(TicketDetail):
    """Customized detail_lyout for Tickets.  Replaces `waiting_for` by
    `faculties`

    """
    main = "general more history_tab more2"
    
    general = dd.Panel("""
    general1:60 comments.CommentsByRFC:30
    """, label=_("General"))

    general1 = """
    summary:40 id:6 
    user:12 end_user:12 deadline
    site topic project 
    workflow_buttons:30 private
    bottom_box
    """

    bottom_box = """
    faculties.DemandsByDemander:20 votes.VotesByVotable:20 clocking.SessionsByTicket:20
    """

    more = dd.Panel("""
    more1 DuplicatesByTicket:20 #WishesByTicket
    description:30 upgrade_notes:20 LinksByTicket:20  
    """, label=_("More"))

    more2 = dd.Panel("""
    deploy.DeploymentsByTicket
    uploads.UploadsByController
    """, label=_("Even more"))

Tickets.detail_layout = TicketDetail()

Sites.detail_layout = """
id name partner #responsible_user
remark
#InterestsBySite TicketsBySite deploy.MilestonesBySite
"""



@dd.receiver(dd.post_analyze)
def my_details(sender, **kw):
    sender.modules.system.SiteConfigs.set_detail_layout("""
    site_company next_partner_id:10
    default_build_method
    """)

