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

    def assigned_to_changed(self, ar):
        """Add a star"""
        self.add_change_watcher(self.assigned_to)

    def end_user_changed(self, ar):
        """Add a star"""
        self.add_change_watcher(self.end_user)

    def user_changed(self, ar):
        """Add a star"""
        self.add_change_watcher(self.user)

    def site_changed(self, ar):
        """Leaves a sub-star of old site, but that's OK for now"""
        if self.site is not None:
            print "Change"
            self.site.add_child_stars(self.site, self)
            # self.add_change_watcher(star.user)

    def after_ui_create(self, ar):
        print "Create"
        self.site_changed(ar)
        self.assigned_to_changed(ar)
        self.end_user_changed(ar)
        self.user_changed(ar)
        super(Ticket, self).after_ui_create(ar)

        if dd.is_installed('notify'):
            ctx = dict(user=ar.user, what=ar.obj2memo(self))
            def msg(user, mm):
                subject = _("{user} submitted ticket {what}").format(**ctx)
                return (E.tostring(E.span(subject)), E.tostring(E.span(subject)))

            mt = rt.actors.notify.MessageTypes.change # Maybe something else, but unimporant
            # owner = self.get_change_owner()
            # rt.models.notify.Message.emit_message(
            #     ar, owner, mt, msg, self.get_change_observers())
            rt.models.notify.Message.emit_message(
                ar, self, mt, msg,
                [(u, u.mail_mode) for u in rt.models.users.User.objects.all()
                    if u.user_type is not None and u.user_type.has_required_roles((rt.modules.tickets.Triager,))
                    and u != ar.get_user()
                 ]
            )


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
    stars.AllStarsByController
    uploads.UploadsByController 
    """, label=_("Even more"))

Tickets.detail_layout = TicketDetail()
Tickets.params_layout = """user end_user assigned_to not_assigned_to interesting_for site project state deployed_to
    has_project show_assigned show_active show_deployed show_todo show_private
    start_date end_date observed_event topic #feasable_by has_ref"""
Tickets.column_names = 'id summary:50 user:10 topic #faculty ' \
                       'workflow_buttons:30 site:10 project:10 *'
MyTickets.params_layout = """
    user end_user site project state
    start_date end_date observed_event topic #feasable_by show_active"""
# Sites.detail_layout = """
# id name partner #responsible_user
# remark
# #InterestsBySite TicketsBySite deploy.MilestonesBySite
# """



