# -*- coding: UTF-8 -*-
# Copyright 2017-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Database models for this plugin.

"""

from lino.api import dd, _

from lino_xl.lib.cal.models import *
from lino_xl.lib.working.choicelists import ReportingTypes
from lino_xl.lib.working.ui import load_sessions, TOTAL_KEY


# class Day(Day):
#     def __init__(self, *args, **kwargs):
#         super(Day, self).__init__(*args, **kwargs)
#         self.sar = self.ar.spawn(rt.models.working.MySessionsByDay, master_instance=self)
#         load_sessions(self, self.sar)
#
#
# class Days(Days, dd.VentilatingTable):
#
#     # column_names_template = 'day_number long_date detail_link description {vcolumns}'
#     column_names_template = 'detail_link worked_tickets {vcolumns} *'
#
#     @dd.displayfield(_("Tickets"))
#     def worked_tickets(self, obj, ar):
#         # pv = dict(start_date=obj.day, end_date=obj.day)
#         # pv.update(observed_event=dd.PeriodEvents.active)
#         # pv.update(user=ar.param_values.user)
#         # sar = ar.spawn(MySessionsByDate, param_values=pv)
#         # elems = [obj.sar.ar2button(label=six.text_type(obj))]
#         elems = []
#         tickets = [
#             ar.obj2html(t, "#{0}".format(t.id), title=t.summary)
#             for t in obj._tickets]
#         if len(tickets) > 0:
#             # elems.append(" (")
#             elems += join_elems(tickets, ', ')
#             # elems.append(")")
#         return E.span(*elems)
#
#     # @dd.displayfield("Date")
#     # def date(cls, row, ar):
#     #     return dd.fdl(row.day)
#
#     @classmethod
#     def param_defaults(cls, ar, **kw):
#         kw = super(Days, cls).param_defaults(ar, **kw)
#         kw.update(start_date=dd.today(-7))
#         kw.update(end_date=dd.today())
#         kw.update(user=ar.get_user())
#         return kw
#
#     @classmethod
#     def get_ventilated_columns(cls):
#
#         def w(rpttype, verbose_name):
#             def func(fld, obj, ar):
#                 return obj._root2tot.get(rpttype, None)
#
#             return dd.VirtualField(dd.DurationField(verbose_name), func)
#
#         for rpttype in ReportingTypes.objects():
#             yield w(rpttype, six.text_type(rpttype))
#         # yield w(None, _("N/A"))
#         yield w(TOTAL_KEY, _("Total"))
#
#
# class DayDetail(dd.DetailLayout):
#     main = "working.MySessionsByDay cal.PlannerByDay"
#
#


class Event(Event, ContactRelated):
    class Meta:
        app_label = 'cal'
        abstract = dd.is_abstract_model(__name__, 'Event')

dd.update_field(Event, 'user', verbose_name=_("Author"))
dd.update_field(Event, 'company', verbose_name=_("Organizer"))
dd.update_field(Event, 'contact_person', verbose_name=_("Contact person"))


class RoomDetail(dd.DetailLayout):
    main = """
    id name
    company contact_person
    description
    cal.EntriesByRoom
    """

# Rooms.set_detail_layout(RoomDetail())

class EventDetail(EventDetail):
    start = "start_date start_time"
    end = "end_date end_time"
    main = "general GuestsByEvent"
    general = dd.Panel("""
    event_type:20 summary:60 id
    start end access_class #all_day #assigned_to #duration #state
    user room company contact_person
    project owner workflow_buttons
    # owner created:20 modified:20
    description #blogs.EntriesByController #outbox.MailsByController
    """, label=_("General"))

# Events.set_detail_layout(EventDetail())
