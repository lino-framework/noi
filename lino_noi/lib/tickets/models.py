# -*- coding: UTF-8 -*-
# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Database models specific for the Team variant of Lino Noi.

Defines a customized :class:`TicketDetail`.

"""
from __future__ import print_function

from lino_xl.lib.tickets.models import *
from lino.modlib.users.mixins import Assignable
from lino.api import _

from lino_xl.lib.working.choicelists import ReportingTypes, ZERO_DURATION
from lino.modlib.summaries.mixins import Summarizable


def get_summary_fields():
    for t in ReportingTypes.get_list_items():
        yield t.name + '_hours'


class Ticket(Ticket, Assignable, Summarizable):

    class Meta(Ticket.Meta):
        # app_label = 'tickets'
        abstract = dd.is_abstract_model(__name__, 'Ticket')

    def assigned_to_changed(self, ar):
        """Add a star and send notification of Assignment"""
        # self.add_change_watcher(self.assigned_to)

        if (self.assigned_to is not None and
                self.assigned_to != ar.user and
                dd.is_installed('notify')):
            ctx = dict(user=ar.user, what=ar.obj2memo(self))
            def msg(user, mm):
                subject = _("{user} has assigned you to ticket: {what}").format(**ctx)
                return (subject , tostring(E.span(subject)))

            mt = rt.models.notify.MessageTypes.tickets

            rt.models.notify.Message.emit_notification(
                ar, self, mt, msg,
                [(self.assigned_to, self.assigned_to.mail_mode)]
            )
    # def end_user_changed(self, ar):
    #     """Add a star"""
    #     self.add_change_watcher(self.end_user)

    # def user_changed(self, ar):
    #     """Add a star"""
    #     self.add_change_watcher(self.user)

    def after_ui_create(self, ar):
        # print("Create")
        # self.site_changed(ar)
        # self.assigned_to_changed(ar)
        # self.end_user_changed(ar)
        # self.user_changed(ar)
        super(Ticket, self).after_ui_create(ar)

        if dd.is_installed('notify'):
            ctx = dict(user=ar.user, what=ar.obj2memo(self))
            def msg(user, mm):
                subject = _("{user} submitted ticket {what}").format(**ctx)
                return (subject , tostring(E.span(subject)))

            mt = rt.models.notify.MessageTypes.tickets
            # owner = self.get_change_owner()
            # rt.models.notify.Message.emit_notification(
            #     ar, owner, mt, msg, self.get_change_observers())
            rt.models.notify.Message.emit_notification(
                ar, self, mt, msg,
                [(u, u.mail_mode) for u in rt.models.users.User.objects.all()
                    if u.user_type and u.user_type.has_required_roles(
                            [Triager])
                    and u != ar.get_user()
                 ]
            )

    show_commits = dd.ShowSlaveTable('github.CommitsByTicket')
    show_changes = dd.ShowSlaveTable('changes.ChangesByMaster')
    # show_wishes = dd.ShowSlaveTable('deploy.DeploymentsByTicket')
    # show_stars = dd.ShowSlaveTable('stars.AllStarsByController')

    @classmethod
    def get_layout_aliases(cls):
        yield ("SUMMARY_FIELDS", ' '.join(get_summary_fields()))

    @classmethod
    def get_summary_master_model(cls):
        return cls

    def reset_summary_data(self):
        for k in get_summary_fields():
            setattr(self, k, ZERO_DURATION)

    def get_summary_collectors(self):
        qs = rt.models.working.Session.objects.filter(ticket=self)
        yield (self.add_from_session, qs)

    def add_from_session(self, obj):
        d = obj.get_duration()
        if d:
            rt = obj.get_reporting_type()
            k = rt.name + '_hours'
            value = getattr(self, k) + d
            setattr(self, k, value)


class TicketDetail(TicketDetail):
    """Customized detail_layout for Tickets in Noi

    """
    main = "general more #history_tab #more2 #github.CommitsByTicket"
    
    general = dd.Panel("""
    general1:60 comments.CommentsByRFC:30
    """, label=_("General"))

    general1 = """
    general1a:30 general1b:30
    """

    # 50+6=56
    # in XL: label span is 4, so we have 8 units for the fields
    # 56.0/8 = 7
    # summary:  50/56*8 = 7.14 --> 7
    # id:  6/56*8 = 0.85 -> 1
    general1a = """
    summary id:6
    site ticket_type 
    workflow_buttons
    description
    """
    general1b = """
    user end_user
    assigned_to private:10
    priority:10 planned_time
    SUMMARY_FIELDS
    working.SessionsByTicket
    """

    more = dd.Panel("""
    more1 DuplicatesByTicket:20 #WishesByTicket
    upgrade_notes LinksByTicket uploads.UploadsByController 
    """, label=_("More"))

    # history_tab = dd.Panel("""
    # changes.ChangesByMaster #stars.StarsByController:20
    # github.CommitsByTicket
    # """, label=_("History"), required_roles=dd.login_required(Triager))

    
    more1 = """
    created modified fixed_since #reported_for #fixed_date #fixed_time
    state ref duplicate_of deadline
    # standby feedback closed
    """

    # more2 = dd.Panel("""
    # # deploy.DeploymentsByTicket
    # # skills.DemandsByDemander
    # stars.AllStarsByController
    # uploads.UploadsByController 
    # """, label=_("Even more"))

class TicketInsertLayout(dd.InsertLayout):
    main = """
    summary #private:20
    right:30 left:50
    """

    right = """
    ticket_type 
    priority
    end_user
    #assigned_to
    #site
    """

    left = """
    description
    """
    
    window_size = (80, 20)


class SiteDetail(SiteDetail):

    main = """general config history"""

    general = dd.Panel("""
    gen_left:20 TicketsBySite:60
    """, label=_("General"))

    gen_left = """
    overview
    SubscriptionsBySite 
    """

    general2 = """
    ref name id 
    company contact_person reporting_type 
    remark:20 workflow_buttons:20
    """
    
    config = dd.Panel("""
    general2
    description 
    """, label=_("Configure"), required_roles = dd.login_required(TicketsStaff)
)

    history = dd.Panel("""
    # meetings.MeetingsBySite
    working.SummariesBySite
    """, label=_("History"))


# Note in the following lines we don't subclass Tickets because then
# we would need to also override these attributes for all subclasses

Tickets.insert_layout = 'tickets.TicketInsertLayout'
Tickets.params_layout = """user end_user assigned_to not_assigned_to interesting_for site has_site state priority
    #deployed_to show_assigned show_active #show_deployed show_todo show_private
    start_date end_date observed_event #topic #feasable_by has_ref"""
Tickets.column_names = 'id summary:50 #user:10 #topic #faculty priority ' \
                       'workflow_buttons:30 site:10 #project:10'
Tickets.tablet_columns = "id summary workflow_buttons"
#Tickets.tablet_columns_popin = "site project"

Tickets.mobile_columns = "workflow_buttons"
#Tickets.mobile_columns_pop = "summary workflow_buttons"
Tickets.popin_columns = "summary"

Tickets.order_by = ["-id"]

MyTickets.params_layout = """
    user end_user site #project state priority
    start_date end_date observed_event #topic #feasable_by show_active"""
MyTickets.column_names = "priority detail_link planned_time SUMMARY_FIELDS workflow_buttons *"

TicketsBySite.column_names = "priority detail_link planned_time SUMMARY_FIELDS workflow_buttons *"
# Sites.detail_layout = """
# id name partner #responsible_user
# remark
# #InterestsBySite TicketsBySite deploy.MilestonesBySite
# """


# Not needed, have it be inffered by mobile_columns or tablet_columns if both None, use normal grid.
#AllTickets.display_mode = "responsive_grid"


