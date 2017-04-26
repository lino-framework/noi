# -*- coding: UTF-8 -*-
# Copyright 2016-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""User interface for this plugin.


"""
import six

from lino_xl.lib.cal.utils import when_text
from lino_xl.lib.clocking.ui import *
from lino.api import _

from django.db.models import Q


from lino_xl.lib.tickets.models import Project
from lino_xl.lib.tickets.ui import Tickets, Projects
# from lino_xl.lib.courses.desktop import Courses
from lino_xl.lib.tickets.models import Ticket
from lino_xl.lib.clocking.roles import Worker
from lino_xl.lib.clocking.choicelists import ReportingTypes

class TOTAL_KEY(object):
    pass

def load_sessions(self, sar):
    self._root2tot = {}
    self._tickets = set()
    grand_tot = Duration()
    for ses in sar:
        self._tickets.add(ses.ticket)
        d = ses.get_duration() or MIN_DURATION
        grand_tot += d
        # root = ses.get_root_project()
        root = ses.get_reporting_type()
        # if ses.ticket:
        #     root = ses.ticket.reporting_type
        # else:
        #     root = None
        tot = self._root2tot.get(root, Duration()) + d
        self._root2tot[root] = tot

    self._root2tot[TOTAL_KEY] = grand_tot


def compute_invested_time(obj, **spv):
    # spv = dict(start_date=pv.start_date, end_date=pv.end_date)
    spv.update(observed_event=dd.PeriodEvents.started)
    sar = SessionsByTicket.request(master_instance=obj, param_values=spv)
    tot = Duration()
    for obj in sar:
        d = obj.get_duration()
        if d is not None:
            tot += d
    return tot


class InvestedTime(dd.Table):
    @dd.virtualfield(dd.DurationField(_("Time")))
    def invested_time(cls, obj, ar):
        return obj._invested_time

    @dd.displayfield(_("Description"))
    def my_description(cls, obj, ar):
        mi = ar.master_instance
        if mi is None:
            return
        lst = [obj.summary]
        tpl = u"{0}: {1}"
        # if obj.site is not None and obj.site == mi.interesting_for:
        #     lst.append(_("site-specific"))
        if obj.site is not None:  # and obj.site != mi.interesting_for:
            lst.append(tpl.format(
                ensureUtf(_("Site")), ensureUtf(obj.site)))
        if obj.user is not None:
            lst.append(tpl.format(
                ensureUtf(_("Author")), ensureUtf(obj.user)))
        if obj.project is not None:
            lst.append(tpl.format(
                ensureUtf(_("Project")), ensureUtf(obj.project)))
        if obj.topic is not None:
            lst.append(tpl.format(
                ensureUtf(_("Topic")), ensureUtf(obj.topic)))
        return E.p(*join_elems(lst, '. '))


def rpttype2vf(func, rpttype, verbose_name):
    return dd.VirtualField(dd.DurationField(verbose_name), func)

MySessionsByDate.column_names = (
    'start_time end_time break_time duration summary ticket '
    'ticket__project workflow_buttons *')

from lino.core.tables import VentilatedColumns

class WorkedHours(dd.VentilatingTable):
    """A table showing one row per day with a summary view of the sesions
    on that day."""
    required_roles = dd.login_required(Worker)
    label = _("Worked hours")
    hide_zero_rows = True
    parameters = ObservedPeriod(
        user=dd.ForeignKey('users.User', null=True, blank=True))
    params_layout = "start_date end_date user"
    # editable = False
    auto_fit_column_widths = True

    class Row(object):
        def __init__(self, ar, day):
            self.day = day
            pv = dict(start_date=day, end_date=day)
            pv.update(observed_event=dd.PeriodEvents.started)
            pv.update(user=ar.param_values.user)
            self.sar = ar.spawn(MySessionsByDate, param_values=pv)
            load_sessions(self, self.sar)
            
        def __unicode__(self):
            return when_text(self.day)

    @dd.displayfield(_("Description"))
    def description(self, obj, ar):
        # pv = dict(start_date=obj.day, end_date=obj.day)
        # pv.update(observed_event=dd.PeriodEvents.active)
        # pv.update(user=ar.param_values.user)
        # sar = ar.spawn(MySessionsByDate, param_values=pv)
        elems = [obj.sar.ar2button(label=six.text_type(obj))]
        tickets = [
            ar.obj2html(t, "#{0}".format(t.id), title=t.summary)
            for t in obj._tickets]
        if len(tickets) > 0:
            elems.append(" (")
            elems += join_elems(tickets, ', ')
            elems.append(")")
        return E.p(*elems)

    @classmethod
    def get_data_rows(cls, ar):
        pv = ar.param_values
        start_date = pv.start_date or dd.today(-7)
        end_date = pv.end_date or dd.today(7)
        d = end_date
        while d > start_date:
            yield cls.Row(ar, d)
            d -= ONE_DAY

    @dd.displayfield("Date")
    def date(cls, row, ar):
        return dd.fdl(row.day)

    @classmethod
    def param_defaults(cls, ar, **kw):
        kw = super(WorkedHours, cls).param_defaults(ar, **kw)
        kw.update(start_date=dd.today(-7))
        kw.update(end_date=dd.today())
        kw.update(user=ar.get_user())
        return kw

    @classmethod
    def get_ventilated_columns(cls):

        def w(rpttype, verbose_name):
            def func(fld, obj, ar):
                return obj._root2tot.get(rpttype, None)
            return dd.VirtualField(dd.DurationField(verbose_name), func)
            
        for rpttype in ReportingTypes.objects():
            yield w(rpttype, six.text_type(rpttype))
        # yield w(None, _("N/A"))
        yield w(TOTAL_KEY, _("Total"))


    @classmethod
    def unused_get_ventilated_columns(cls):
        Project = rt.models.tickets.Project

        def w(prj, verbose_name):
            # return a getter function for a RequestField on the given
            # EntryType.

            def func(fld, obj, ar):
                return obj._root2tot.get(prj, None)

            return dd.VirtualField(dd.DurationField(verbose_name), func)

        for p in Project.objects.filter(parent__isnull=True).order_by('ref'):
            yield w(p, six.text_type(p))
        yield w(None, _("Total"))



class DurationReport(VentilatedColumns):
    
    abstract = True
    
    @classmethod
    def get_ventilated_columns(cls):
        def w(rpttype, verbose_name):
            def func(fld, obj, ar):
                return obj._root2tot.get(rpttype, None)
            return dd.VirtualField(dd.DurationField(verbose_name), func)
        
        # def w(rpttype, verbose_name):
        #     def func(fld, obj, ar):
        #         if obj.get_reporting_type() == rpttype:
        #             return obj.get_duration()
        #         return None
        #     return dd.VirtualField(dd.DurationField(verbose_name), func)
            
        for rpttype in ReportingTypes.objects():
            yield w(rpttype, six.text_type(rpttype))
        # yield w(None, _("N/A"))

class SessionsByReport(Sessions, DurationReport):
    master = 'clocking.ServiceReport'
    
    column_names_template = "start_date start_time end_time break_time " \
                            "my_description:50 #session_type {vcolumns}"

    # @classmethod
    # def get_data_rows(cls, ar):
    #     for ses in cls.get_request_queryset(ar):
    #         load_sessions(ses, [ses])
    #         yield ses

    @classmethod
    def get_request_queryset(self, ar):
        mi = ar.master_instance
        if mi is None:
            return
        spv = dict(start_date=mi.start_date, end_date=mi.end_date)
        # spv = mi.get_tickets_parameters()
        spv.update(company=mi.interesting_for)
        ar.param_values.update(spv)

        qs = super(SessionsByReport, self).get_request_queryset(ar)
        for obj in qs:
            load_sessions(obj, [obj])
            # obj._invested_time = compute_invested_time(
            #     obj, start_date=mi.start_date, end_date=mi.end_date,
            #     user=mi.user)
            if obj._root2tot.get(TOTAL_KEY):
                yield obj

    @dd.displayfield(_("Description"))
    def my_description(self, obj, ar):
        elems = [obj.summary]
        t = obj.ticket
        elems += [" ", 
            ar.obj2html(t, "#{0}".format(t.id), title=t.summary)]
        return E.p(*elems)

class TicketsByReport(Tickets, DurationReport):
    """The list of tickets mentioned in a service report."""
    master = 'clocking.ServiceReport'
    # column_names = "summary id reporter project product site state
    # invested_time"
    column_names_template = "id overview project state {vcolumns}"
    order_by = ['id']

    @classmethod
    def get_request_queryset(self, ar):
        mi = ar.master_instance
        if mi is None:
            return
        pv = ar.param_values

        pv.update(start_date=mi.start_date, end_date=mi.end_date)
        pv.update(interesting_for=mi.interesting_for)
        pv.update(observed_event=TicketEvents.clocking)

        spv = dict(start_date=mi.start_date, end_date=mi.end_date)
        spv.update(observed_event=dd.PeriodEvents.started)
        spv.update(user=mi.user)
        qs = super(TicketsByReport, self).get_request_queryset(ar)
        for obj in qs:
            sar = SessionsByTicket.request(
                master_instance=obj, param_values=spv)
            load_sessions(obj, sar)
            # obj._invested_time = compute_invested_time(
            #     obj, start_date=mi.start_date, end_date=mi.end_date,
            #     user=mi.user)
            if obj._root2tot.get(TOTAL_KEY):
                yield obj


class ProjectsByReport(Projects, DurationReport):
    """The list of projects mentioned in a service report.
    
    """
    master = 'clocking.ServiceReport'
    column_names_template = "ref name active_tickets {vcolumns}"
    order_by = ['ref']

    @classmethod
    def get_request_queryset(self, ar):

        mi = ar.master_instance
        if mi is None:
            return
        
        pv = ar.param_values
        pv.update(start_date=mi.start_date, end_date=mi.end_date)
        pv.update(interesting_for=mi.interesting_for)
       
        spv = dict(start_date=mi.start_date, end_date=mi.end_date)
        spv.update(observed_event=dd.PeriodEvents.started)
        spv.update(user=mi.user)
        
        qs = super(ProjectsByReport, self).get_request_queryset(ar)
        for obj in qs:
            # spv.update(project=obj)
            sar = Sessions.request(
                param_values=spv,
                filter=Q(ticket__project=obj))
            load_sessions(obj, sar)
            if obj._root2tot.get(TOTAL_KEY):
                yield obj
            
    @classmethod
    def old_get_request_queryset(self, ar):
        Tickets = rt.modules.tickets.Tickets
        mi = ar.master_instance
        if mi is None:
            return

            
        def worked_time(**spv):
            tot = Duration()
            tickets = []
            spv = mi.get_tickets_parameters(**spv)
            spv.update(observed_event=TicketEvents.clocking)
            sar = Tickets.request(param_values=spv)
            for ticket in sar:
                ttot = compute_invested_time(
                    ticket, start_date=mi.start_date, end_date=mi.end_date,
                    user=mi.user)
                if ttot:
                    tot += ttot
                    tickets.append(ticket)
            return tot, tickets

        projects_list = []
        children_time = {}

        qs = super(ProjectsByReport, self).get_request_queryset(ar)
        for prj in qs:
            tot, tickets = worked_time(project=prj)
            prj._tickets = tickets
            prj._invested_time = tot
            projects_list.append(prj)
            if tot:
                p = prj.parent
                while p is not None:
                    cht = children_time.get(p.id, Duration())
                    children_time[p.id] = cht + tot
                    p = p.parent

        # compute children_time for each project
        for prj in projects_list:
            prj._children_time = children_time.get(prj.id, Duration())
            # p = prj.parent
            # ct = Duration()
            # while p is not None:
            #     ct += children_time.get(p.id, Duration())

        # remove projects that have no time at all
        def f(prj):
            return prj._invested_time or prj._children_time
        projects_list = filter(f, projects_list)

        # add an unsaved Project for the tickets without project:
        tot, tickets = worked_time(has_project=dd.YesNo.no)
        if tot:
            prj = rt.modules.tickets.Project(name="(no project)")
            prj._tickets = tickets
            prj._invested_time = tot
            prj._children_time = Duration()
            projects_list.append(prj)
        return projects_list

    @dd.displayfield(_("Tickets"))
    def active_tickets(cls, obj, ar):
        lst = []
        for ticket in obj._tickets:
            lst.append(ar.obj2html(
                ticket, text="#%d" % ticket.id, title=six.text_type(ticket)))
        return E.p(*join_elems(lst, ', '))



# class CoursesByReport(Courses, DurationReport):
#     """The list of courses mentioned in a service report.
#
#     """
#     master = 'clocking.ServiceReport'
#     column_names_template = "start_date name * {vcolumns}"
#     order_by = ['start_date']
#
#     @classmethod
#     def get_request_queryset(self, ar):
#
#         mi = ar.master_instance
#         if mi is None:
#             return
#
#         pv = ar.param_values
#         pv.update(start_date=mi.start_date, end_date=mi.end_date)
#         pv.update(interesting_for=mi.interesting_for)
#
#         spv = dict(start_date=mi.start_date, end_date=mi.end_date)
#         spv.update(observed_event=dd.PeriodEvents.started)
#         spv.update(user=mi.user)
#         spv.update(company=mi.company)
#
#         qs = super(CoursesByReport, self).get_request_queryset(ar)
#         for obj in qs:
#             sar = Sessions.request(param_values=spv)
#             load_sessions(obj, sar)
#             if obj._root2tot.get(TOTAL_KEY):
#                 yield obj
#
    

class ServiceReports(dd.Table):
    """List of service reports."""
    required_roles = dd.login_required(Worker)

    model = "clocking.ServiceReport"
    detail_layout = """
    start_date end_date user interesting_for ticket_state printed
    company contact_person
    SessionsByReport
    # TicketsByReport
    # ProjectsByReport
    # CoursesByReport
    """
    column_names = "start_date end_date user interesting_for "\
                   "ticket_state printed *"

    params_panel_hidden = True
    


class ReportsByPartner(ServiceReports):
    """List of service reports issued for a given site."""
    master_key = 'interesting_for'


# @dd.receiver(dd.post_save, sender=Project)
# def my_setup_columns(sender, **kw):
#     WorkedHours.setup_columns()
#     settings.SITE.kernel.must_build_site_cache()

# # moved to xl.clocking.mixins.py
# @dd.receiver(dd.post_save, sender=Ticket)
# def on_ticket_create(sender, instance=None, created=False, **kwargs):
#     if settings.SITE.loading_from_dump:
#         return
#     me = instance.user
#     if created and me is not None and me.open_session_on_new_ticket:
#         ses = rt.modules.clocking.Session(ticket=instance, user=me)
#         ses.full_clean()
#         ses.save()

