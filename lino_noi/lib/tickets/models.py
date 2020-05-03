# -*- coding: UTF-8 -*-
# Copyright 2016-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Database models specific for the Team variant of Lino Noi.

Defines a customized :class:`TicketDetail`.

"""

from lino.api import _
from lino.modlib.users.mixins import Assignable
from lino.modlib.summaries.mixins import Summarized
from lino_xl.lib.tickets.models import *
from lino_xl.lib.working.choicelists import ReportingTypes, ZERO_DURATION


def get_summary_fields():
    for t in ReportingTypes.get_list_items():
        yield t.name + '_hours'

class Site(Site):

    class Meta(Site.Meta):
        app_label = 'tickets'
        abstract = dd.is_abstract_model(__name__, 'Site')

    def get_change_observers(self, ar=None):
        action = ar.bound_action.action if ar.bound_action else None
        if ar is not None and isinstance(action, CreateRow) and issubclass(ar.actor.model,Ticket):
            subs = rt.models.groups.Group.objects.filter(site=ar.selected_rows[-1].site)
            #subs = rt.models.tickets.Subscription.objects.filter(site=ar.selected_rows[-1].site)
            for s in subs.members.all():
                for (u, um) in [(u, u.mail_mode) for u in [sub.user for sub in s]
                                if (u.user_type and u.user_type.has_required_roles([Triager])
                                    and u != ar.get_user())]:
                    yield (u, um)
        else:
            #for s in rt.models.tickets.Subscription.objects.filter(site=self):
            for s in rt.models.groups.Group.objects.filter(site=self):
                for sub in s.members.all():
                    yield (sub.user, sub.user.mail_mode)

    #def after_ui_create(self, ar):
    #    super(Site, self).after_ui_create(ar)
    #    rt.models.tickets.Subscription.objects.create(user=ar.get_user(), site=self)


class Ticket(Ticket, Assignable, Summarized):

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

    show_commits = dd.ShowSlaveTable('github.CommitsByTicket')
    show_changes = dd.ShowSlaveTable('changes.ChangesByMaster')
    # show_wishes = dd.ShowSlaveTable('deploy.DeploymentsByTicket')
    # show_stars = dd.ShowSlaveTable('stars.AllStarsByController')


    def get_change_subject(self, ar, cw):
        ctx = dict(user=ar.user, what=str(self))
        if cw is None:
            return _("{user} submitted ticket {what}").format(**ctx)
        if len(list(cw.get_updates())) == 0:
            return
        return _("{user} modified {what}").format(**ctx)

    def get_change_body(self, ar, cw):
        ctx = dict(user=ar.user, what=ar.obj2memo(self))
        if cw is None:
            elems = [E.p(
                _("{user} submitted ticket {what}").format(**ctx), ".")]
            elems += list(self.get_change_info(ar, cw))
        else:
            items = list(cw.get_updates_html(["_user_cache"]))
            if len(items) == 0:
                return
            elems = []
            elems += list(self.get_change_info(ar, cw))
            elems.append(E.p(
                _("{user} modified {what}").format(**ctx), ":"))
            elems.append(E.ul(*items))
        # print("20170210 {}".format(tostring(E.div(*elems))))
        return tostring(E.div(*elems))

    @classmethod
    def get_layout_aliases(cls):
        yield ("SUMMARY_FIELDS", ' '.join(get_summary_fields()))

    # @classmethod
    # def get_summary_master_model(cls):
    #     return cls

    def reset_summary_data(self):
        for k in get_summary_fields():
            setattr(self, k, ZERO_DURATION)
        self.last_commenter = None

    def get_summary_collectors(self):
        qs = rt.models.working.Session.objects.filter(ticket=self)
        yield (self.add_from_session, qs)
        qs = rt.models.comments.Comment.objects.filter(**gfk2lookup(rt.models.comments.Comment._meta.get_field("owner"),
                                                                    self)
                                                       ).order_by("-created")[0:1]
        yield (self.add_from_comment, qs)

    def add_from_comment(self, obj):
        self.last_commenter = obj.user

    def add_from_session(self, obj):
        d = obj.get_duration()
        if d:
            rt = obj.get_reporting_type()
            k = rt.name + '_hours'
            value = getattr(self, k) + d
            setattr(self, k, value)\

    @dd.chooser()
    def site_choices(cls, ar):
        # if user is None:
        #     user = ar.get_user()
        user = ar.get_user()
        # user = user if user is not None else ar.get_user()
        group_ids = rt.models.groups.Membership.objects.filter(user=user).values_list("group__pk", flat=True)
        # user_ids = [user.pk]
        # if end_user: user_ids.append(end_user.pk)
        # pks = rt.models.tickets.Subscription.objects.filter(user__pk__in=user_ids).values_list("site__pk", flat=True)
        # # print(pks)
        # return Site.objects.filter(id__in=pks)
        return Site.objects.filter(group__in=group_ids)


class TicketDetail(TicketDetail):
    """Customized detail_layout for Tickets in Noi

    """
    main = "general more comments.CommentsByMentioned #history_tab #more2 #github.CommitsByTicket"

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
    LinksByTicket
    """
    general1b = """
    user end_user
    quick_assign_to private:10
    priority:10 planned_time
    SUMMARY_FIELDS
    working.SessionsByTicket
    """

    more = dd.Panel("""
    more1 DuplicatesByTicket:20 #WishesByTicket
    upgrade_notes description uploads.UploadsByController
    """, label=_("More"))

    # history_tab = dd.Panel("""
    # changes.ChangesByMaster #stars.StarsByController:20
    # github.CommitsByTicket
    # """, label=_("History"), required_roles=dd.login_required(Triager))


    more1 = """
    created modified fixed_since #reported_for #fixed_date #fixed_time
    state assigned_to ref duplicate_of deadline
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
    site
    """

    left = """
    description
    """

    window_size = (80, 20)


class SiteDetail(SiteDetail):

    main = """general config"""

    general = dd.Panel("""
    gen_left:20 TicketsBySite:60
    """, label=_("General"))

    gen_left = """
    group
    overview
    """

    general2 = """
    ref name
    company contact_person
    reporting_type #start_date end_date hours_paid
    remark:20 private
    workflow_buttons:20 id
    working.SummariesBySite
    """

    config = dd.Panel("""
    general2:50 description:30
    """, label=_("Configure"), required_roles = dd.login_required(TicketsStaff))

    # history = dd.Panel("""
    # # meetings.MeetingsBySite
    # working.SummariesBySite
    # """, label=_("History"))


# Note in the following lines we don't subclass Tickets because then
# we would need to also override these attributes for all subclasses

Tickets.insert_layout = 'tickets.TicketInsertLayout'
Tickets.params_layout = """user end_user assigned_to not_assigned_to interesting_for site has_site state priority
    #deployed_to show_assigned show_active #show_deployed show_todo show_private
    start_date end_date observed_event #topic #feasable_by has_ref
    last_commenter not_last_commenter subscriber"""
Tickets.column_names = 'id summary:50 #user:10 #topic #faculty priority ' \
                       'workflow_buttons:30 site:10 #project:10'
Tickets.tablet_columns = "id summary workflow_buttons"
#Tickets.tablet_columns_popin = "site project"

Tickets.mobile_columns = "workflow_buttons"
#Tickets.mobile_columns_pop = "summary workflow_buttons"
Tickets.popin_columns = "summary"

Tickets.order_by = ["-id"]

TicketsBySite.column_names = "priority detail_link planned_time SUMMARY_FIELDS workflow_buttons *"
AllSites.column_names = "ref name company group remark workflow_buttons id *"
# Sites.detail_layout = """
# id name partner #responsible_user
# remark
# #InterestsBySite TicketsBySite deploy.MilestonesBySite
# """


# Not needed, have it be inffered by mobile_columns or tablet_columns if both None, use normal grid.
#AllTickets.display_mode = "responsive_grid"
